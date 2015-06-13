upstream gamex_app {
    server 127.0.0.1:10000 fail_timeout=0;
    server 127.0.0.1:10001 fail_timeout=0;
    server 127.0.0.1:10002 fail_timeout=0;
    server 127.0.0.1:10003 fail_timeout=0;
    server 127.0.0.1:10004 fail_timeout=0;
    server 127.0.0.1:10005 fail_timeout=0;
    server 127.0.0.1:10006 fail_timeout=0;
    server 127.0.0.1:10007 fail_timeout=0;
    server 127.0.0.1:10008 fail_timeout=0;
}

server {
    listen 80;
    server_name admin.gamex.mobile.youku.com;
    charset utf-8;

    location /static/ {
        # 只允许内网访问
        allow 60.247.104.99; # 办公室的公网IP
        allow 10.10.0.0/16;
        allow 10.0.0.0/8;
        allow 10.10.116.0/24;
        allow 10.10.202.0/24;
        allow 218.30.0.0/16;
        deny all;
        alias /opt/app/python/m-game-platform/app/static/;
        expires 15m;

    }

    location /apkdownload/ {
        alias /opt/data/download/;

    }

    location / {

        # 只允许内网访问
        allow 60.247.104.99; # 办公室的公网IP
        allow 10.10.0.0/16;
        allow 10.0.0.0/8;
        allow 10.10.116.0/24;
        allow 10.10.202.0/24;
        allow 218.30.0.0/16;
        deny all;
        fastcgi_pass gamex_app;
        fastcgi_param PATH_INFO $fastcgi_script_name;
        fastcgi_param REQUEST_METHOD $request_method;
        fastcgi_param QUERY_STRING $query_string;
        fastcgi_param SERVER_NAME $server_name;
        fastcgi_param SERVER_PORT $server_port;
        fastcgi_param SERVER_PROTOCOL $server_protocol;
        fastcgi_param CONTENT_TYPE $content_type;
        fastcgi_param CONTENT_LENGTH $content_length;
        fastcgi_pass_header Authorization;
        fastcgi_intercept_errors off;
    }

}

