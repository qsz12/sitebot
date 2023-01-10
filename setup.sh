exec `sudo apt update -y`
exec `sudo apt install git build-essential -y`

export EC2_AVAIL_ZONE=`curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone`
export EC2_REGION="`echo \"$EC2_AVAIL_ZONE\" | sed 's/[a-z]$//'`"

exec `pip3 install -r requirements.txt`
exec `gunicorn app:app -k=eventlet --bind=0.0.0.0:8080 --access-logfile=- --log-level=INFO &`