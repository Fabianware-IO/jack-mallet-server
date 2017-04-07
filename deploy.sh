#! /bin/bash

SHA1=$1

EB_BUCKET=jackmallet-server
EB_ENVIRONMENT_NAME="JackMallet-Server-Production"
AWS_REGION="us-east-1"

DOCKERRUN_FILE=$SHA1-Dockerrun.aws.json

# Deploy image to dockerhub
docker push fabianwareio/jackmallet-server:$SHA1

# Create new Elastic Beanstalk version
sed "s/<TAG>/$SHA1/" < Dockerrun.aws.json.template > $DOCKERRUN_FILE
aws --region=$AWS_REGION s3 cp $DOCKERRUN_FILE s3://$EB_BUCKET/$DOCKERRUN_FILE
aws --region=$AWS_REGION elasticbeanstalk create-application-version --application-name jackmallet-server \
	--version-label $SHA1 --source-bundle S3Bucket=$EB_BUCKET,S3Key=$DOCKERRUN_FILE

# Update Elastic Beanstalk environment to new version
aws --region=$AWS_REGION elasticbeanstalk update-environment --environment-name $EB_ENVIRONMENT_NAME \
	--version-label $SHA1
