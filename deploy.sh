#! /bin/bash

SHA1=$1

# Deploy image to dockerhub
docker push fabianwareio/jackmallet-server:$SHA1

# Create new Elastic Beanstalk version
EB_BUCKET=jackmallet-server
DOCKERRUN_FILE=$SHA1-Dockerrun.aws.json
sed "s/<TAG>/$SHA1/" < Dockerrun.aws.json.template > $DOCKERRUN_FILE
aws s3 cp $DOCKERRUN_FILE s3://$EB_BUCKET/$DOCKERRUN_FILE
aws --region="us-east-1" elasticbeanstalk create-application-version --application-name jackmallet-server \
	--version-label $SHA1 --source-bundle S3Bucket=$EB_BUCKET,S3Key=$DOCKERRUN_FILE

# Update Elastic Beanstalk environment to new version
aws elasticbeanstalk update-environment --environment-name jackmallet-server-prod \
	--version-label $SHA1
