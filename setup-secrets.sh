#!/bin/bash

# Setup Google Cloud Secret Manager for API keys

PROJECT_ID="your-project-id"

echo "🔐 Setting up Secret Manager for Techline Custom Agent"

# Create secrets (you'll need to provide the actual values)
echo "Creating OPENAI_API_KEY secret..."
echo -n "your-openai-api-key" | gcloud secrets create openai-api-key \
  --replication-policy="automatic" \
  --data-file=-

echo "Creating GOOGLE_MAPS_API_KEY secret..."
echo -n "your-google-maps-api-key" | gcloud secrets create google-maps-api-key \
  --replication-policy="automatic" \
  --data-file=-

# Grant Cloud Run service account access to secrets
echo "🔑 Granting access to secrets..."
gcloud secrets add-iam-policy-binding openai-api-key \
  --member="serviceAccount:$PROJECT_ID-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding google-maps-api-key \
  --member="serviceAccount:$PROJECT_ID-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

echo "✅ Secret Manager setup completed!"
