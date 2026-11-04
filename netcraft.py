import socket
import os
import requests
import shutil
from pathlib import Path
import string
from tqdm import tqdm
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
def EVILGINX_DICTIONARY_LIST_GENERATOR():
    file_path = Path(__file__).with_name('Evilginx_Keywords.txt')
    f = file_path.open('r')
    dictionary_list = [line.strip() for line in f]
    f.close()
    return dictionary_list


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
    common_tlds = ["com", "net", "org", "info", "biz", "co", "us", "uk", "ca", "io", "xyz", "cm", "top", "gg", "cc", "xyz", "ai"]
    mapping = mode_true()
    if advanced_mode > 75:
        tld_list_used = common_tlds #placeholder
    else:
        tld_list_used = common_tlds
    for i, char in enumerate(domain_name):
        if char in mapping:
            for adjacent in mapping[char]:
                for tld in tld_list_used:
                    similar_domains.add(domain_name[:i] + adjacent + domain_name[i + 1:] + '.' + tld)


    for i in range(len(domain_name)):
        omitted = domain_name[:i] + domain_name[i + 1:]
        for tld in tld_list_used:
            similar_domains.add(omitted + '.' + tld)

    
    for i in range(len(domain_name)):
        doubled = domain_name[:i] + domain_name[i] + domain_name[i] + domain_name[i + 1:]
        for tld in tld_list_used:

            similar_domains.add(doubled + '.' + tld)

    #keyword add
    if advanced_mode > 50:
        print("keywords enabled")

        keywords = EVILGINX_DICTIONARY_LIST_GENERATOR()
        
        for tld in tld_list_used:
            for keyword in keywords:
                similar_domains.add(domain_name + '-' + keyword + '.' + tld)
                similar_domains.add(keyword + '-' + domain_name + '.' + tld)
                if advanced_mode > 75:
                    similar_domains.add(domain_name + keyword + '.' + tld)
                    similar_domains.add(keyword + domain_name + '.' + tld)

    
    
    

    #similar_domains.discard(domain)
    return similar_domains


def create_output_file(domain, similar_domains):
    domain_name, extension = domain.rsplit('.', 1)
    filename = f"{domain_name}_similar_domains.html"
    filename2 = "similar_domains.html"
    global domain_status_list
    domain_status_list = []
    ticker_for_more_file_writes = 0
    with open(filename, 'w') as f:
        f.write("<!DOCTYPE html>\n<html>\n<head><title>Similar Domains</title><style>table, th, td { border: 1px solid; border-collapse: collapse; }</style> <body style=\"background-color:#aaaaaa;\"><h1 style=\"color:white;\"></head>\n<body>\n")
        if advanced_mode > 0:
            f.write(f"<h2>advanced: {advanced_mode}, {mode}</h2>\n")
            
        f.write(f"<h1>exisiting similar to {domain}</h1><br><h3>total: {len(similar_domains)}, {len(domain_status_list)}</h3>\n")

        class domain_status:
            def __init__(self, domain, status_code, status_color):
                self.domain = domain
                self.status_code = status_code
                self.status_color = status_color
        
        for d in tqdm(similar_domains, desc="Checking domains"):
            try:
                status_code = requests.head(f"http://{d}", timeout=2).status_code
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
            
            domain_status_list.append(domain_status(d, status_code, status_color))

    
    
        sorted_domain_status_list = sorted(domain_status_list, key=lambda x: (isinstance(x.status_code, str), x.status_code))
        #f.write(f'<span style="color: {status_color}"><a href="http://{d}">{d}</a><br><p>Status: {status_code}</p></span>\n')
        if advanced_mode == 0:
            for domain_status in sorted_domain_status_list:
                f.write(f'<span style="color: {domain_status.status_color}"><a href="http://{domain_status.domain}">{domain_status.domain}</a><br><p>Status: {domain_status.status_code}</p></span>\n')
            f.write("</body>\n</html>\n")
        else:
            f.write(f'<table><tr><th>domain</th><th>status</th></tr>')
            for domain_status in sorted_domain_status_list:
               
                f.write(f'<tr><td><a href="http://{domain_status.domain}">{domain_status.domain}</a></td><td style="color: {domain_status.status_color}">{domain_status.status_code}</td></tr>')
            f.write(f'</table>')
    return filename
    

def get_dictionary_list(domain):
    pass

def main():
    global advanced_mode
    global mode
    domain = input("domain? ").strip().lower()
    advanced_mode = input("advanced mode? (y/n) ").strip().lower()
    if advanced_mode == 'y':
        try:
            advanced_mode = int(input("advancedness? (0-100) ").strip().lower()) 
        except ValueError:
            print("\:(")
            return
        #return
    elif advanced_mode == 'n':
        advanced_mode = 0
        
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        return
    
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
# Source - https://stackoverflow.com/a/61667980
# Posted by Alex Seceleanu
# Retrieved 2026-10-20, License - CC BY-SA 4.0
    src=output_file
    dst="output-domain-status.html"
    shutil.copy(src,dst)

    
    

main()
