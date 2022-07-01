gcloud init
gcloud container clusters create finalproject
gcloud container clusters get-credentials finalproject
kubectl create deployment finalprojectapp --image=ferdmartin/finalprojectapp
kubectl expose deployment finalprojectapp --type=LoadBalancer --port=5003
kubectl get services