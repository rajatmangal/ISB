# Required software
- Docker: https://docs.docker.com/docker-for-windows/ (Windows) or https://docs.docker.com/docker-for-mac/ (Mac)
- Python3 
- Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
- Postgresql & pgadmin: https://www.postgresql.org/download/ & https://www.pgadmin.org/download/

# Instruction to deploy container locally
CD into ISB directory & run the following commands: 
- 'docker-compose build' builds the image for the Django app's container, and download all required python packages.
    * If new packages are added, they need to be added into requirements.txt and execute the command again.
- 'docker-compose run web python manage.py migrate' migrates the application into postgres
    * Should only be run once when first cloning the repo.
- 'docker-compose up' would create container instances for postgres database and the django app and run on port 5432 and port 8000 of localhost, respectively
    * Changes in codes are listened to and applied by Django instantly.

# Step to deploy containers to Azure Kubernetes Service (AKS)
- I'm currently following this tutorial and modify the commands to match our app: https://docs.microsoft.com/en-us/azure/aks/tutorial-kubernetes-prepare-app
- Current status: Implementing manifest (isb-azure.yaml) file for Kubernetes deployment and services (Step 4 in tutorial)
- Other resources for reference: https://medium.com/@markgituma/kubernetes-local-to-production-with-django-2-docker-and-minikube-ba843d858817



