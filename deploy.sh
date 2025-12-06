#!/bin/bash

echo "🚀 KONTROLLZENTRUM DEPLOYMENT"
echo "=============================="

# 1. Build Docker Image
echo "📦 Building Docker image..."
docker build -t kontrollzentrum:latest .

# 2. Push to Registry
echo "📤 Pushing to registry..."
docker tag kontrollzentrum:latest kontrollzentrum:v1.0
docker push kontrollzentrum:latest

# 3. Deploy to Kubernetes
echo "☸️  Deploying to Kubernetes..."
kubectl apply -f kubernetes.yml

# 4. Wait for deployment
echo "⏳ Waiting for deployment..."
kubectl rollout status deployment/kontrollzentrum

# 5. Get service info
echo "✅ Deployment complete!"
kubectl get service kontrollzentrum-service

echo "🎉 KONTROLLZENTRUM IS LIVE!"
