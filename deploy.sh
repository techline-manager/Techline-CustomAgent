#!/bin/bash

# GCP Cloud Run Deployment Script for Techline Custom Agent

# Set your GCP project details
PROJECT_ID="your-project-id"
REGION="us-central1"
SERVICE_NAME="techline-custom-agent"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Deploying Techline Custom Agent to Google Cloud Run"

# Build and push the Docker image
echo "📦 Building Docker image..."
gcloud builds submit --tag $IMAGE_NAME

# Deploy to Cloud Run
echo "🌐 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars PORT=8080 \
  --memory 1Gi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --timeout 300s

echo "✅ Deployment completed!"
echo "🔗 Your API URL:"
gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)'
