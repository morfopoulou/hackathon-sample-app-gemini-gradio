## Starter Kit Gemini App

Starter kit to build an app using Gemini and Gradio Framework.

## Sample app

 https://hackathon-sample-app-615535018443.europe-west3.run.app/

 Follow the steps to build it.

## Clone

git clone https://github.com/morfopoulou/hackathon-sample-app-gemini-gradio.git

## Deploy to Cloud Run

Ensure the default Cloud Run service account (if not specified that will be PROJECT_NUMBER-compute@developer.gserviceaccount.com) has the following IAM permissions:
- Cloud Build Editor
- Logging Admin
- Storage Object User
- Vertex AI User
- Artifact Registry Administrator


Set the environment variables in `initial.sh'
Add your app name in the Dockerfile
```In Cloud Shell, execute the following commands:
gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repository-format=Docker
gcloud auth configure-docker "$GCP_REGION-docker.pkg.dev"
gcloud builds submit --tag "$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME"
```
Before you can push or pull images, configure Docker to use the Google Cloud CLI to authenticate requests to Artifact Registry.
In Cloud Shell, execute the following command to create a Artifact Registry repository:

```
gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repository-format=Docker
```

To set up authentication to Docker repositories in the region us-west1, run the following command:

```
gcloud auth configure-docker "$GCP_REGION-docker.pkg.dev"
```

To build the Docker image of your application and push it to Google Artifact Registry

```
gcloud builds submit --tag "$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME"
```

Now deploy in Cloud Run
``` 
gcloud run deploy "$SERVICE_NAME" \
  --port=8080 \
  --image="$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME" \
  --allow-unauthenticated \
  --region=$GCP_REGION \
  --platform=managed  \
  --project=$GCP_PROJECT \
  --set-env-vars=GCP_PROJECT=$GCP_PROJECT,GCP_REGION=$GCP_REGION,GCP_BUCKET=$GCP_BUCKET
