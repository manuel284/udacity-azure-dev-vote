#!/bin/bash

# Variables
resourceGroup="acdnd-c4-project"
clusterName="udacity-cluster"
location="westeurope"

# Create resource group
echo "Creating Resource Group"

az group create -n $resourceGroup -l $location

echo "Resource Group created"

# Install aks cli
echo "Installing AKS CLI"

az aks install-cli

echo "AKS CLI installed"

# Create AKS cluster
echo "Creating AKS cluster $clusterName"

az aks create \
--resource-group $resourceGroup \
--name $clusterName \
--node-count 1 \
--enable-addons monitoring \
--generate-ssh-keys \
-l $location

echo "AKS cluster created: $clusterName"

# Connect to AKS cluster

echo "Getting AKS credentials"

az aks get-credentials \
--resource-group $resourceGroup \
--name $clusterName \
--verbose

echo "Verifying connection to $clusterName"

kubectl get nodes

echo "Deploying to AKS cluster"

kubectl apply -f azure-vote.yaml



while true; do wget -q -O- 40.113.96.210; done
