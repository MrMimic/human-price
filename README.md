human-price

### Build

    nox -s build

### Build on GCP

Create Docker image

> gcloud builds submit --tag gcr.io/human-price/human-price

Run cloud function

> gcloud run deploy --image gcr.io/human-price/human-price --platform managed --max-instances=2