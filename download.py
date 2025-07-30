import requests
from tqdm import tqdm
import re
import os
import time

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


def download_with_retries(url, filepath, max_retries=3, delay=3):
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, stream=True, timeout=30 * attempt)
            response.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(response.content)
            return True
        except requests.RequestException as e:
            print(f"Attempt {attempt} failed for {filepath}: {e}")
            if attempt < max_retries:
                backoff = delay * (2 ** (attempt - 1))
                print(f"Retrying in {backoff:.1f} seconds...")
                time.sleep(backoff)
            else:
                print(f"Failed to download {filepath} after {max_retries} attempts.")
                return False

def download_files(file_urls, delay=3, max_retries=3):
    # Create folders if they don't exist
    os.makedirs("pdfs", exist_ok=True)
    os.makedirs("txts", exist_ok=True)

    for file in tqdm(file_urls, desc="Downloading files", unit="file"):
        year = file.get('year')
        base_url = file.get('url')

        if not year or not base_url:
            print("Skipping due to missing 'year' or 'url'.")
            continue

        # PDF
        pdf_url = f"{base_url}.pdf"
        pdf_path = os.path.join("pdfs", f"{year}.pdf")
        download_with_retries(pdf_url, pdf_path, max_retries, delay)

        time.sleep(delay)

        # TXT
        txt_url = f"{base_url}.texteBrut"
        txt_path = os.path.join("txts", f"{year}.txt")
        download_with_retries(txt_url, txt_path, max_retries, delay)

        time.sleep(delay)



def main():
    catalogue_url = 'https://gallica.bnf.fr/ark:/12148/cb344120051/date'
    catalogue_file = get_catalogue(catalogue_url)
    file_urls = parse_catalogue(catalogue_file)
    download_files(file_urls)

if __name__ == "__main__":
    main()

