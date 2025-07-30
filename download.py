import requests
import json
import re

def get_catalogue(url):
    # use wget to download the catalogue file
    response = requests.get(url)
    return response.text

def parse_catalogue(file):
    # regex for matching the JSON-like structure in the file
    pattern = r'\{\\?"display\\?":true,\\?"active\\?":true,\\?"parameters\\?":\{.*?\},\\?"contenu\\?":\\?"1 numéro\\?",\\?"description\\?":\\?"\d{4}\\?",\\?"selected\\?":false,\\?"url\\?":\\?"https://gallica\.bnf\.fr/ark:/12148/[a-z0-9]+\\?",\\?"etat\\?":\\?"\\?"\}'
    matches = re.findall(pattern, file)

    field_pattern = r'"description":"(\d{4})".*?"url":"(https://gallica\.bnf\.fr/ark:/12148/[a-z0-9]+)"'

    # Now extract year + url from each
    results = []
    for block in matches:
        # Remove escape backslashes for proper matching
        clean_block = block.replace('\\"', '"')
        match = re.search(field_pattern, clean_block)
        if match:
            year, url = match.groups()
            results.append({
                'year': year,
                'url': url
            })
    assert len(matches) == len(results), "Mismatch in number of matches and results"
    return results

def download_files(file_urls):
    pass



def main():
    catalogue_url = 'https://gallica.bnf.fr/ark:/12148/cb344120051/date'
    catalogue_file = get_catalogue(catalogue_url)
    file_urls = parse_catalogue(catalogue_file)
    download_files(file_urls)

if __name__ == "__main__":
    main()

