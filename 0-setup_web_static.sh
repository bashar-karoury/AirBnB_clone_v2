#!/usr/bin/env bash
# Shell Script to set up the server for the deployment of web_static

package="nginx"

# Check if the nginx is installed
if ! dpkg -l | grep -q "^ii  $package"; then
    sudo apt-get update
    sudo apt-get install -y $package
fi

#create /data directory if not exist
mkdir -p /data
mkdir -p /data/web_static
mkdir -p /data/web_static/releases
mkdir -p /data/web_static/shared
mkdir -p /data/web_static/releases/test/
content="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
ubuntu@89-web-01:~/$ curl localhost/hbnb_static/index.html
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"

echo "$content" > /data/web_static/releases/test/index.html
ln -sfr /data/web_static/releases/test/ /data/web_static/current
user="ubuntu"
group="ubuntu"

# Change the ownership of the directory
sudo chown -R $user:$group /data

nginx_config="/etc/nginx/sites-available/default"
web_static_dir="/data/web_static/current"

# Update Nginx configuration
sudo tee $nginx_config > /dev/null <<EOF
server {
    listen 80;
    server_name static_web;
    root /data/web_static;
    location / {
        try_files \$uri \$uri/ =404;
    }

    location /hbnb_static/ {
        alias $web_static_dir/;
	try_files \$uri \$uri/ =404;
    }
}
EOF

# Test Nginx configuration
sudo nginx -t

# Restart Nginx to apply changes
sudo service nginx restart
