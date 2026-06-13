import requests
import zipfile
import re
import sys
from google.cloud import storage

URL = "https://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS92_V202601.zip"
DESTINATION = "/data/BACI_HS92_V202601.zip"
YEAR_START = 1995
YEAR_END = 2024
BUCKET_NAME = "trade-flow-analysis-raw"
SOURCE_FILE_NAME = "/data/extracted/BACI_HS92_Y1995_V202601.csv"
DESTINATION_BLOB_NAME = "BACI_HS92_Y1995_V202601.csv"


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

def is_in_year_range(name, year_start, year_end):
    m = re.search(r"_Y(\d{4})_", name)
    return m is not None and year_start <= int(m.group(1)) <= year_end

def extract_zip(zip_path, dest_dir):
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        wanted = [n for n in names if is_in_year_range(n, YEAR_START, YEAR_END) or n.startswith(("country_codes", "product_codes"))]
        for name in wanted:
            z.extract(name, path=dest_dir)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )




if __name__ == "__main__":


    upload_blob(
        bucket_name=sys.argv[1],
        source_file_name=sys.argv[2],
        destination_blob_name=sys.argv[3],
    )