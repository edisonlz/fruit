upstream tornado {
    server 127.0.0.1:9000 fail_timeout=0;
    server 127.0.0.1:9001 fail_timeout=0;
    server 127.0.0.1:9002 fail_timeout=0;
    server 127.0.0.1:9003 fail_timeout=0;
}

server {
    listen 100;
    server_name 10.105.28.41;
    charset utf-8;

#    location /static/ {
#        alias /opt/app/python/m-cms-new/app/static/;
#    }

    location / {
	    allow 60.247.104.99; # 办公室的公网IP
        allow 211.157.171.226;
	    allow 10.10.0.0/16;
 	    allow 10.10.116.0/24;
        allow 10.10.202.0/24;
	    allow 218.30.0.0/16;
	    deny all;
        proxy_pass          http://tornado;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

}