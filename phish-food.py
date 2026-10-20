import os
import socket

# Define a keyboard adjacency map
KEYBOARD_ADJACENCY = {
    'q': ['w', 'a'], 'w': ['q', 'e', 's'], 'e': ['w', 'r', 'd'], 'r': ['e', 't', 'f'],
    't': ['r', 'y', 'g'], 'y': ['t', 'u', 'h'], 'u': ['y', 'i', 'j'], 'i': ['u', 'o', 'k'],
    'o': ['i', 'p', 'l'], 'p': ['o'], 'a': ['q', 's', 'z'], 's': ['a', 'd', 'w', 'x'],
    'd': ['s', 'f', 'e', 'c'], 'f': ['d', 'g', 'r', 'v'], 'g': ['f', 'h', 't', 'b'],
    'h': ['g', 'j', 'y', 'n'], 'j': ['h', 'k', 'u', 'm'], 'k': ['j', 'l', 'i'],
    'l': ['k', 'o'], 'z': ['a', 'x'], 'x': ['z', 'c', 's'], 'c': ['x', 'v', 'd'],
    'v': ['c', 'b', 'f'], 'b': ['v', 'n', 'g'], 'n': ['b', 'm', 'h'], 'm': ['n', 'j'],
    '1': ['2', 'q'], '2': ['1', '3', 'w'], '3': ['2', '4', 'e'], '4': ['3', '5', 'r'],
    '5': ['4', '6', 't'], '6': ['5', '7', 'y'], '7': ['6', '8', 'u'], '8': ['7', '9', 'i'],
    '9': ['8', '0', 'o'], '0': ['9', 'p']
}

# Fetch all TLDs dynamically
def get_all_tlds():
    try:
        with open("tlds-alpha-by-domain.txt", "r") as file:
            tlds = [line.strip().lower() for line in file if not line.startswith("#")]
        return tlds
    except FileNotFoundError:
        return ["com", "net", "org", "info", "biz", "co", "us", "uk", "ca", "io", "xyz", "cm"]

# Generate permutations with substitutions
def generate_similar_domains(domain):
    domain_name, extension = domain.split('.')
    similar_domains = set()
    all_tlds = get_all_tlds()

    for i, char in enumerate(domain_name):
        if char in KEYBOARD_ADJACENCY:
            for adjacent in KEYBOARD_ADJACENCY[char]:
                for tld in all_tlds:
                    similar_domains.add(domain_name[:i] + adjacent + domain_name[i + 1:] + '.' + tld)

        if char == 'o':
            for tld in all_tlds:
                similar_domains.add(domain_name[:i] + '0' + domain_name[i + 1:] + '.' + tld)
        elif char == 'i':
            for tld in all_tlds:
                similar_domains.add(domain_name[:i] + '1' + domain_name[i + 1:] + '.' + tld)

    for i in range(len(domain_name)):
        doubled = domain_name[:i] + domain_name[i] + domain_name[i] + domain_name[i + 1:]
        for tld in all_tlds:
            similar_domains.add(doubled + '.' + tld)

    return similar_domains

# Check if a domain exists
def check_domain_existence(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

# Example usage
domain = input("domain?")
similar_domains = list(generate_similar_domains(domain))

# Ensure file is saved in the current working directory
output_path = os.path.join(os.getcwd(), "phish.txt")

# Separate domains by existence status
existing_domains = []
non_existing_domains = []

total_domains = len(similar_domains)
for index, d in enumerate(similar_domains):
    if check_domain_existence(d):
        existing_domains.append(d)
    else:
        non_existing_domains.append(d)
    
    # Print progress
    progress = ((index + 1) / total_domains) * 100
    print(f"Progress: {progress:.2f}% ({index + 1}/{total_domains})", end="\r")

# Write to the file
with open(output_path, "w") as file:
    file.write("Existing Domains:\n")
    file.write("\n".join(existing_domains))
    file.write("\n" + "-" * 40 + "\n")
    file.write("Non-Existing Domains:\n")
    file.write("\n".join(non_existing_domains))

print(f"\nDomains and their statuses written to {output_path}")
