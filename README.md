Steps to run the project.

1. Clone the repo to the local.
2. run 'source env/Scripts/activate' to start the virtual environemnt.
3. run 'python manage.py runserver'
4. visit 'localhost/devices' to get the list of devices present in the API. On the same page there is option to add the new devices. You can also modify the Device details directly in the  API.


Steps to setup Lambda for AWS deployment: 

1. update settings.py in the project for the environ setup:

import environ
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
env = environ.Env()
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=True)
if READ_DOT_ENV_FILE:
    env.read_env(str(ROOT_DIR / '.env'))
    
2. update manage.py with the following lines:

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_aws_lambda.production')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    
3. create a folder utils inside django_aws_lambda
    create storages.py file inside utils folder with the following lines:

from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False

4. set environment variable with a path to Django local configuration file

export DJANGO_SETTINGS_MODULE=django_aws_lambda.local

5. Create serverless configuration

    initialize npm:

npm init

    install serverless

npm install -g serverless

    install serverless plugins

npm install -P serverless-dotenv-plugin
npm install -P serverless-prune-plugin
npm install -P serverless-python-requirements
npm install -P serverless-wsgi

6. create serverless.yaml file with the following configuration:

service: django-aws-lambda

plugins:
  - serverless-dotenv-plugin
  - serverless-prune-plugin
  - serverless-python-requirements
  - serverless-wsgi
useDotenv: true

custom:
  dotenv:
    logging: false
  pythonRequirements:
    dockerizePip: non-linux
    zip: true
    fileName: requirements.txt
  stage: ${env:STAGE}
  wsgi:
    app: django_aws_lambda.wsgi.application
    packRequirements: false
  prune:
    automatic: true
    number: 3

functions:
  - app:
      handler: wsgi_handler.handler
      events:
        - http: ANY /
        - http: ANY /{proxy+}
      timeout: 30

provider:
  name: aws
  role: arn:aws:iam::<role_id>:role/<role_name>
  profile: <your-profile-name>  # make sure that you configured aws profile using `aws configure --profile <your-profile-name>`
  region: us-east-1
  runtime: python3.8
  versionFunctions: false
  stage: ${env:STAGE}
  timeout: 60
  vpc:
    securityGroupIds:
      - <your-security-group-id>
      - <your-security-group-id>
    subnetIds:
      - <your-subnet-id>
      - <your-subnet-id>
  deploymentBucket:
    name: ${env:DEPLOYMENT_BUCKET}
  apiGateway:
    shouldStartNameWithService: true
  lambdaHashingVersion: 20201221

package:
  individually:
    true
  exclude:
    - .env
    - .git/**
    - .github/**
    - .serverless/**
    - static/**
    - .cache/**
    - .pytest_cache/**
    - node_modules/**

7. Use Docker for deploying your Django project to AWS Lambda using Serverless

    run Amazon Linux 2 docker image:

docker run -it -v $(pwd):/root/src/ -v /Users/<your_user>/.aws:/root/.aws amazonlinux:latest bash

    install the necessary Unix dependencies:

yum install sudo -y
sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel wget tar sqlite-devel gcc-c++ make

    install node.js version 14:

curl -sL https://rpm.nodesource.com/setup_14.x | sudo -E bash - 
sudo yum install -y nodejs

    install Python 3.8.7:

cd /opt
sudo wget https://www.python.org/ftp/python/3.8.7/Python-3.8.7.tgz
sudo tar xzf Python-3.8.7.tgz
cd Python-3.8.7
sudo ./configure --enable-optimizations
sudo make altinstall
sudo rm -f /opt/Python-3.8.7.tgz

    create python and pip aliases:

alias python='python3.8'
alias pip='pip3.8'

    update pip and setuptools:

pip install --upgrade pip setuptools

    install serverless:

npm install -g serverless

    move to project directory

cd /root/src/

    install requirements inside docker container:

pip install -r requirements.txt

    set environment variable with a path to django production configuration file

export DJANGO_SETTINGS_MODULE=django_aws_lambda.production

    migrate database changes

python manage.py migrate

  
  
 Once the migration is done, Project will be available at this URL:
https://<some-id>.execute-api.<your-aws-region>.amazonaws.com/
  
