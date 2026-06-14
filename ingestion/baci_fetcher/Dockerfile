FROM python:3.12.13-slim

WORKDIR /app

# deps first — this layer caches unless requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# both the fetcher and the loader live in this one image
COPY fetch_baci.py .
COPY load_to_bigquery.py .

# default command is the fetcher; the DAG overrides it for the load step
CMD ["python", "fetch_baci.py"]