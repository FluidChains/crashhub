#!/bin/sh

while [ ! -f /etc/letsencrypt/live/crashhub/fullchain.pem ]
do
        echo "sleeping"
        sleep 5
done

echo $NGINX_HOST
/bin/bash -c "envsubst < /etc/nginx/conf.d/CrashhubSSL.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"
