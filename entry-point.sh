#!/bin/bash

echo "Migrate the Database"

# Run flask migrate
echo "Run flask migrate"
flask db migrate
   
echo 2

# Upgrade db
flask db upgrade

# Run flask server
echo "Run web server"
gunicorn --reload -c config/gunicorn_conf.py wsgi