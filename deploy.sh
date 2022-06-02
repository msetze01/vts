#!/bin/sh
BUCKET="vts-deployment-temp"

aws s3 mb s3://$BUCKET
sam build -t template.yaml
sam deploy --stack-name vts-api-stack --capabilities CAPABILITY_IAM --s3-bucket $BUCKET
