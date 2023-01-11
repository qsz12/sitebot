#!/usr/bin/env bash

# running apt update and upgrade, to be sure everything is up to the mark
sudo apt update -y
sudo apt install git build-essential python3-pip -y

# setting an EC2 env var
export EC2_AVAIL_ZONE=`curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone`
export EC2_REGION="`echo \"$EC2_AVAIL_ZONE\" | sed 's/[a-z]$//'`"

sudo pip install -r requirements.txt

# running the server and detaching
gunicorn app:app -k=eventlet --bind=0.0.0.0:8080 --access-logfile=- --log-level=INFO &
