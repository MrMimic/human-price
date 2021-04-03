human-price

### Build

    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install poetry
    poetry install

### Build on GCP

Create Docker image

> gcloud builds submit --tag gcr.io/human-price/human-price

Run cloud function

> gcloud run deploy --image gcr.io/human-price/human-price --platform managed