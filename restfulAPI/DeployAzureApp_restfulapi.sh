az group create --name cisc5550finalproject --location eastus
az container create --resource-group cisc5550finalproject --name restfulapi --image ferdmartin/finalprojectrestapi --dns-name-label cisc5550fernando --ports 5001
az container show --resource-group cisc5550finalproject --name restfulapi --query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState}" --out table