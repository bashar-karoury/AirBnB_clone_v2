#!/usr/bin/env bash
# Shell Script to set up the server for the deployment of web_static
package="nginx"

# Check if the nginx is installed
if ! dpkg -l | grep -q "^ii  $package"; then
    sudo apt-get update
    sudo apt-get install -y $package
fi

mkdir -p /data/web_static/shared
mkdir -p /data/web_static/releases/test/
content="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"

echo "$content" > /data/web_static/releases/test/index.html
rm -f  /data/web_static/current
ln -sfr /data/web_static/releases/test/ /data/web_static/current
user="ubuntu"
group="ubuntu"

# Change the ownership of the directory
sudo chown -hR $user /data
sudo chgrp -hR $group /data
nginx_config="/etc/nginx/sites-available/default"
web_static_dir="/data/web_static/current"

# Update Nginx configuration
sudo tee $nginx_config > /dev/null <<EOF
server {
    listen 80;
    server_name static_web;
    root /;
    location / {
        try_files \$uri \$uri/ =404;
	add_header X-Served-By \$hostname;
    }

    location /hbnb_static {
        alias $web_static_dir/;
	try_files \$uri \$uri/ =404;
	add_header X-Served-By \$hostname;
    }
}
EOF

# Test Nginx configuration
sudo nginx -t > /dev/null 2>&1

# Restart Nginx to apply changes
sudo service nginx start > /dev/null 2>&1
