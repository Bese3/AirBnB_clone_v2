#!/usr/bin/env bash
# a Bash script that sets up web servers for the deployment of web_static
sudo apt update
sudo apt-get install -y nginx
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html
sudo chmod a+w /data/web_static/releases/test/index.html
echo "testing server configration" > /data/web_static/releases/test/index.html
sudo ln -sf  /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data
sudo sed -i "s-\tserver_name _;-\tserver_name _;\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n-" /etc/nginx/sites-available/default
sudo sed -i "s-\tserver_name _;-\tserver_name _;\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n-" /etc/nginx/sites-enabled/default
sudo service nginx restart
