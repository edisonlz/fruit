upstream cms_new_app {
    server 127.0.0.1:10005 fail_timeout=0;
}

server {
    listen 90;
    server_name 10.105.28.41;
    charset utf-8;

    location /static/ {
        alias /opt/app/python/m-cms-new/app/static/;
    }

    location / {
#        proxy_pass  http://cms_new_app;
#        proxy_connect_timeout 3;
#        proxy_send_timeout 3;
#        proxy_read_timeout 3;
#        proxy_redirect      default;
#         #  proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
#          # proxy_set_header    X-Real-IP $x_remote_addr;
#        proxy_set_header    Host $http_host;
#        proxy_set_header    Range $http_range;
        # 只允许内网访问
	allow 60.247.104.99; # 办公室的公网IP
        allow 211.157.171.226;
	allow 10.10.0.0/16;
 	allow 10.10.116.0/24;
        allow 10.10.202.0/24;
	allow 218.30.0.0/16;
	deny all;
        fastcgi_pass cms_new_app;
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