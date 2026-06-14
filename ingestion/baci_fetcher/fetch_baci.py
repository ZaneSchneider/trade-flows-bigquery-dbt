import requests
import zipfile
import re
from google.cloud import storage
import os

URL = "https://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS92_V202601.zip"
YEAR_START = 1995
YEAR_END = 2024
BUCKET_NAME = "trade-flow-analysis-raw"
DATA_DIR = "./data"  


def download_large_file(url, destination):
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
        print("File downloaded successfully!")
    except requests.exceptions.RequestException as e:
        print("Error downloading the file:", e)
        raise 


def is_in_year_range(name, year_start, year_end):
    m = re.search(r"_Y(\d{4})_", name)
    return m is not None and year_start <= int(m.group(1)) <= year_end


def extract_zip(zip_path, dest_dir):
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()

        wanted = [
            n for n in names 
            if is_in_year_range(n, YEAR_START, YEAR_END) 
            or os.path.basename(n).startswith(("country_codes", "product_codes"))
        ]

        for name in wanted:
            z.extract(name, path=dest_dir)
        return wanted


def upload_blob(bucket, source_file_name, destination_blob_name):
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


def main():

    zip_path = os.path.join(DATA_DIR, "BACI_HS92_V202601.zip")
    extract_dir = os.path.join(DATA_DIR, "extracted")
    os.makedirs(DATA_DIR, exist_ok=True)

    download_large_file(URL, zip_path)

    extracted = extract_zip(zip_path, extract_dir)

    bucket = storage.Client().bucket(BUCKET_NAME)
    for name in extracted:
        local_path = os.path.join(extract_dir, name)
        blob_name = f"baci/{os.path.basename(name)}"
        upload_blob(bucket, local_path, blob_name)


if __name__ == "__main__":

    main()