# MSD - Homework
 Alejandro V.

## Prerequisites
This demo uses a Dynamodb table to run it you can use the template.yaml with AWS SAM CLI to create it.
```bash
sam validate
sam build
sam deploy --stack-name msd
# To delete the table 
sam delete --stack-name msd
```

 ## Usage Locally (without docker)
 ```bash
export REGION="eu-central-1"
export FETCH_FREQUENCY=300
export DATABASE_TABLE="msd-prices"
export COINGECKO_BASE_URL="https://api.coingecko.com/api/v3/simple"
virtualenv venv # assuming you are using env
cd application
flask --app bitcoin run --port 5001
```

## Usage Locally (docker)
```bash
docker build -t flask-microservice .
docker run -p 5000:5000 flask-microservice
```

## Launch New Service Task in the Cluster
```bash
sam validate --template cluster.yaml
sam build --template cluster.yaml
sam deploy --stack-name msdService --template cluster.yaml --capabilities CAPABILITY_IAM --region eu-central-1
# To delete the cluster
sam delete --stack-name msdService --region eu-central-1
```