import requests

def get_catalogue(url):
    # use wget to download the catalogue file
    response = requests.get(url)
    return response.text

def parse_catalogue(file):
    pass

def download_files(file_urls):
    pass



def main():
    catalogue_url = 'https://gallica.bnf.fr/ark:/12148/cb344120051/date'
    catelogue_file = get_catalogue(catalogue_url)
    file_urls = parse_catalogue(catelogue_file)
    download_files(file_urls)

if __name__ == "__main__":
    main()

