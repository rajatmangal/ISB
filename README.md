# Required softwares
- Docker: https://docs.docker.com/docker-for-windows/ (Windows) or https://docs.docker.com/docker-for-mac/ (Mac)
- Python3 
- Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
- Postgresql & pgadmin: https://www.postgresql.org/download/ & https://www.pgadmin.org/download/

# Resources
- Azure Tutorial: https://docs.microsoft.com/en-us/azure/aks/tutorial-kubernetes-prepare-app
- Deployment of Django app with Postgres on Kubernetes: https://medium.com/@markgituma/kubernetes-local-to-production-with-django-3-postgres-with-migrations-on-minikube-31f2baa8926e
- Defining container starting order: https://medium.com/@xcoulon/initializing-containers-in-order-with-kubernetes-18173b9cc222

# To start container locally for development
- CD into ISB directory (where Dockerfile & docker-compose.yaml is located) before running these command
- 'docker-compose build' builds the image for the Django app's container, and download all required python packages.
    * Any changes in terms of logic, settings or dependencies require executing this command again.
    * For any additional dependencies, ie. python packages, add them into requirements.txt and follow the convention there (name >= versionRequired)

- 'docker-compose up' would create container instances for postgres database and the django app and run on port 5432 and port 8000 of localhost, respectively
    * Changes in front-end codes are listened to and applied by Django (no rebuild image requires).

# To apply of database schema locally (any modifications for database, tables)
- 'docker-compose run web python manage.py makemigrations'
- 'docker-compose run web python manage.py migrate'
- 'docker-compose run web python manage.py createsuperuser'

# To deploy containers to Azure Kubernetes Service (AKS) 
Note: These steps are quite manual right now, and I'm trying to figure out a more streamline ways to execute the whole process.
1. Create Container Registry and push the container images
- Before starting the process, make sure the container image is latest up-to-date (by running docker-compose build)
- 'docker images' to displays all container images 
    * In this case, the images for the app are called isb-image, and the database is postgres
- 'az group create --name cmpt-474 --location canadacentral' creates a new resource group on Azure 
    * Azure resource group is a logical container into which Azure resources are deployed and managed.
    * Only needs to be created once.
- 'az acr create --resource-group cmpt-474 --name <acrName> --sku Basic' creates a new Azure Container Registry (ACR)
    * Container registry is the repository where images are pushed for deployment
    * ACR only needs to be created once, and subsequent images can be pushed there next
- 'az acr list --resource-group cmpt-474 --query "[].{acrLoginServer:loginServer}" --output table' retrieves acrLoginServer name
    * Copy the output somewhere conveniently - you need to use this acrLoginServer many times.

(For these steps, repeat for postgres image - however should only need to do once)
- 'docker tag isb-image <acrLoginServer>/isb-image:v1' to tag the container image
    * v1 stands for version 1. If this is not the first version of the image on ACR, name them accordingly
- 'docker images' to display the images again, now with the newly tagged images we just created.
- 'docker push <acrLoginServer>/imageName>:v1 to push your images onto the ACR. Might take a while
- 'az acr repository show-tags --name <acrName> --repository isb-image --output table' to view all the versions of images that is on ACR.

2. Create a Kubernetes cluster and connect to it
- 'az aks create --resource-group cmpt-474 --name <clusterName> --node-count 2 --generate-ssh-keys --attach-acr <acrName>'
    * This deploys a new Azure cluster, it will take a few minutes.
- 'az aks install-cli' installs the kubectl command-line tool for interacting with Kubernetes.
- 'az aks get-credentials --resource-group cmpt-474 --name <clusterName>' configures connection between your kubectl and the cluster

3. YAML files and deployment
- In the repo, these .yaml files 'db-persistent-vol.yaml', 'db-secret.yaml', 'db-deployment.yaml', 'isb.yaml' define how the deployments of the containers works (for details, refer to the Medium tutorial link)
- Modify the following lines:
    * In db-deployment.yaml, line 18: Change it to "image: <acrLoginServer>:postgres:v1"
    * In isb.yaml, line 19: Change it to "image: <acrLoginServer>:postgres:v1"
    * In isb.yaml, line 25: Change it to "image: <acrLoginServer>:isb-image:<tag>"
- 'kubectl apply -f db-persistent-vol.yaml -f db-secret.yaml -f db-deployment.yaml -f isb.yaml' 
    * creates the deployments for the application and database
- 'kubectl get pods' displays the pods name, there should be two of them - 1 for the isb application and 1 for postgres
- 'kubectl get service isb --watch' would show the isb application's external IP for access
    * Access the ip_addr:8000 should displays the application.
- If it throws an error of "[IP address] disallowed host":
    * Edit settings.py to add the addresses into ALLOWED_HOSTS 
    * Rebuild, push the isb image again and run the kubectl apply command again 
4. Database schema changes (Or when application are first deployed to cluster):
- 'kubectl exec -it <isbPodName> -- /bin/bash' opens a bash shell on the isb container
- Then executes the docker-compose commands like in local changes
    * These needs to be executed when application first deployed, because the database tables are not yet created.






