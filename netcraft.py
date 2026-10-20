import socket
import os
import requests

ADJACENCY = {
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
LOOKALIKES = {
    'o': ['0'], 'i': ['l', '1'], 'l': ['1', 'i'], 's': ['5'], 'z': ['2'], 'b': ['6', '8'],
    'g': ['9'], 'q': ['9'], 'a': ['4'], 'e': ['3'], 'rn': ['m'], 'vv': ['w']

}
mode = '100'


def mode_true():
    if mode == 'A':
        return ADJACENCY
    if mode == 'L':
        return LOOKALIKES
    if mode == '100':
        return {**ADJACENCY, **LOOKALIKES}


def domain_existence(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False


def generate_similar_domains(domain):
    if '.' not in domain:
        raise ValueError(f"'{domain}' doesn't look like a valid domain (missing TLD)")

    domain_name, extension = domain.rsplit('.', 1)
    similar_domains = set()
    #tlds = get_all_tlds()
    common_tlds = ["com", "net", "org", "info", "biz", "co", "us", "uk", "ca", "io", "xyz", "cm"]
    mapping = mode_true()

    for i, char in enumerate(domain_name):
        if char in mapping:
            for adjacent in mapping[char]:
                for tld in common_tlds:
                    similar_domains.add(domain_name[:i] + adjacent + domain_name[i + 1:] + '.' + tld)

    for i in range(len(domain_name)):
        doubled = domain_name[:i] + domain_name[i] + domain_name[i] + domain_name[i + 1:]
        for tld in common_tlds:

            similar_domains.add(doubled + '.' + tld)

    similar_domains.discard(domain)
    return similar_domains


def create_output_file(domain, similar_domains):
    domain_name, extension = domain.rsplit('.', 1)
    filename = f"{domain_name}_similar_domains.html"
    filename2 = "similar_domains.html"

    with open(filename, 'w') as f:
        f.write("<!DOCTYPE html>\n<html>\n<head><title>Similar Domains</title></head>\n<body>\n")
        f.write(f"<h1>exisiting similar to {domain}</h1>\n")
        for d in sorted(similar_domains):
            try:
                status_code = requests.head(f"http://{d}").status_code
            except requests.exceptions.RequestException:
                status_code = "DNE"
            if status_code == 200:
                status_color = "#00ff00"
            elif status_code == 404:
                status_color = "#ff0000"
            elif status_code == "DNE":
                status_color = "#900010"
            else:
                status_color = "#ffff00"
            f.write(f'<span style="color: {status_color}"><a href="http://{d}">{d}</a><br><p>Status: {status_code}</p></span>\n')
        f.write("</body>\n</html>\n")

    return filename
    

def get_dictionary_list(domain):
    pass

def main():
    domain = input("domain? ").strip().lower()
    if domain_existence(domain):
        similar_domains = generate_similar_domains(domain)
        output_file = create_output_file(domain, similar_domains)
        print(f"Checking {len(similar_domains)} candidate domains, saving results to   {os.path.abspath(output_file)}")
    else:
        print(f"'{domain}' doesn't resolve — check the spelling and try again.")
        #for similar_domain in similar_domains:
        #    if domain_existence(similar_domain) == True:
         #       print(f"{similar_domain} exists.")
   # else:
    #    print(f"'{domain}' doesn't resolve — check the spelling and try again.")
    
    

main()
