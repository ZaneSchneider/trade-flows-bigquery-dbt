FROM python:3.12.13-slim

WORKDIR /app

# deps first — this layer caches unless requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# then app code
COPY fetch_baci.py .

CMD ["python", "fetch_baci.py"]