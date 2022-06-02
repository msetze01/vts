#!/bin/sh
BUCKET="vts-deployment-temp"
aws cloudformation delete-stack --stack-name vts-api-stack
aws s3 rb s3://$BUCKET --force
