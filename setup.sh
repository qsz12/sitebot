exec `sudo apt install git build-essential`

export EC2_AVAIL_ZONE=`curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone`
export EC2_REGION="`echo \"$EC2_AVAIL_ZONE\" | sed 's/[a-z]$//'`"

exec `git clone https://github.com/essnine/sitebot`

cd sitebot
exec `pip install -r requirements.txt`