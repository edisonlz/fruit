upstream cms_api {
    server 127.0.0.1:10001 fail_timeout=0;
    server 127.0.0.1:10002 fail_timeout=0;
    server 127.0.0.1:10003 fail_timeout=0;
    server 127.0.0.1:10004 fail_timeout=0;
    server 127.0.0.1:10005 fail_timeout=0;
    server 127.0.0.1:10006 fail_timeout=0;
    server 127.0.0.1:10007 fail_timeout=0;
    server 127.0.0.1:10008 fail_timeout=0;
    server 127.0.0.1:10009 fail_timeout=0;
    server 127.0.0.1:10010 fail_timeout=0;
}

server {
    listen 100;
    #server_name cms.m.youku.com;
    charset utf-8;

    set $x_remote_addr $http_x_real_ip;
    if ($x_remote_addr = "") {
        set $x_remote_addr $remote_addr;
    }

    #location /static/ {
    #    alias /opt/app/python/m-cms-new/api/static/;
    #}

    location / {
        proxy_pass          http://cms_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }
}


