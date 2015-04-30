upstream sdk_user_api {
    server 127.0.0.1:10000 fail_timeout=0;
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
    server 127.0.0.1:10011 fail_timeout=0;
    server 127.0.0.1:10012 fail_timeout=0;
    server 127.0.0.1:10013 fail_timeout=0;
    server 127.0.0.1:10014 fail_timeout=0;
    server 127.0.0.1:10015 fail_timeout=0;
    server 127.0.0.1:10016 fail_timeout=0;
    server 127.0.0.1:10017 fail_timeout=0;
    server 127.0.0.1:10018 fail_timeout=0;
    server 127.0.0.1:10019 fail_timeout=0;
    server 127.0.0.1:10020 fail_timeout=0;
    server 127.0.0.1:10021 fail_timeout=0;
    server 127.0.0.1:10022 fail_timeout=0;
    server 127.0.0.1:10023 fail_timeout=0;
    server 127.0.0.1:10024 fail_timeout=0;
    server 127.0.0.1:10025 fail_timeout=0;
    server 127.0.0.1:10026 fail_timeout=0;
    server 127.0.0.1:10027 fail_timeout=0;
    server 127.0.0.1:10028 fail_timeout=0;
    server 127.0.0.1:10029 fail_timeout=0;
    server 127.0.0.1:10030 fail_timeout=0;
    server 127.0.0.1:10031 fail_timeout=0;
    server 127.0.0.1:10032 fail_timeout=0;
    server 127.0.0.1:10033 fail_timeout=0;
    server 127.0.0.1:10034 fail_timeout=0;
    server 127.0.0.1:10035 fail_timeout=0;
    server 127.0.0.1:10036 fail_timeout=0;
    server 127.0.0.1:10037 fail_timeout=0;
    server 127.0.0.1:10038 fail_timeout=0;
    server 127.0.0.1:10039 fail_timeout=0;
    server 127.0.0.1:10040 fail_timeout=0;
    server 127.0.0.1:10041 fail_timeout=0;
    server 127.0.0.1:10042 fail_timeout=0;
    server 127.0.0.1:10043 fail_timeout=0;
    server 127.0.0.1:10044 fail_timeout=0;
    server 127.0.0.1:10045 fail_timeout=0;
    server 127.0.0.1:10046 fail_timeout=0;
    server 127.0.0.1:10047 fail_timeout=0;
    server 127.0.0.1:10048 fail_timeout=0;
    server 127.0.0.1:10049 fail_timeout=0;
    server 127.0.0.1:10050 fail_timeout=0;
    server 127.0.0.1:10051 fail_timeout=0;
    server 127.0.0.1:10052 fail_timeout=0;
    server 127.0.0.1:10053 fail_timeout=0;
    server 127.0.0.1:10054 fail_timeout=0;
    server 127.0.0.1:10055 fail_timeout=0;
    server 127.0.0.1:10056 fail_timeout=0;
    server 127.0.0.1:10057 fail_timeout=0;
    server 127.0.0.1:10058 fail_timeout=0;
    server 127.0.0.1:10059 fail_timeout=0;
    server 127.0.0.1:10060 fail_timeout=0;
    server 127.0.0.1:10061 fail_timeout=0;
    server 127.0.0.1:10062 fail_timeout=0;
    server 127.0.0.1:10063 fail_timeout=0;
    server 127.0.0.1:10064 fail_timeout=0;
    server 127.0.0.1:10065 fail_timeout=0;
    server 127.0.0.1:10066 fail_timeout=0;
    server 127.0.0.1:10067 fail_timeout=0;
    server 127.0.0.1:10068 fail_timeout=0;
    server 127.0.0.1:10069 fail_timeout=0;
    server 127.0.0.1:10070 fail_timeout=0;
    server 127.0.0.1:10071 fail_timeout=0;
    server 127.0.0.1:10072 fail_timeout=0;
    server 127.0.0.1:10073 fail_timeout=0;
    server 127.0.0.1:10074 fail_timeout=0;
    server 127.0.0.1:10075 fail_timeout=0;
    server 127.0.0.1:10076 fail_timeout=0;
    server 127.0.0.1:10077 fail_timeout=0;
    server 127.0.0.1:10078 fail_timeout=0;
    server 127.0.0.1:10079 fail_timeout=0;
    server 127.0.0.1:10080 fail_timeout=0;
    server 127.0.0.1:10081 fail_timeout=0;
    server 127.0.0.1:10082 fail_timeout=0;
    server 127.0.0.1:10083 fail_timeout=0;
    server 127.0.0.1:10084 fail_timeout=0;
    server 127.0.0.1:10085 fail_timeout=0;
    server 127.0.0.1:10086 fail_timeout=0;
    server 127.0.0.1:10087 fail_timeout=0;
    server 127.0.0.1:10088 fail_timeout=0;
    server 127.0.0.1:10089 fail_timeout=0;
    server 127.0.0.1:10090 fail_timeout=0;
    server 127.0.0.1:10091 fail_timeout=0;
    server 127.0.0.1:10092 fail_timeout=0;
    server 127.0.0.1:10093 fail_timeout=0;
    server 127.0.0.1:10094 fail_timeout=0;
    server 127.0.0.1:10095 fail_timeout=0;
    server 127.0.0.1:10096 fail_timeout=0;
    server 127.0.0.1:10097 fail_timeout=0;
    server 127.0.0.1:10098 fail_timeout=0;
    server 127.0.0.1:10099 fail_timeout=0;
    server 127.0.0.1:10100 fail_timeout=0;
    server 127.0.0.1:10101 fail_timeout=0;
    server 127.0.0.1:10102 fail_timeout=0;
    server 127.0.0.1:10103 fail_timeout=0;
    server 127.0.0.1:10104 fail_timeout=0;
    server 127.0.0.1:10105 fail_timeout=0;
    server 127.0.0.1:10106 fail_timeout=0;
    server 127.0.0.1:10107 fail_timeout=0;
    server 127.0.0.1:10108 fail_timeout=0;
    server 127.0.0.1:10109 fail_timeout=0;
    server 127.0.0.1:10110 fail_timeout=0;
    server 127.0.0.1:10111 fail_timeout=0;
    server 127.0.0.1:10112 fail_timeout=0;
    server 127.0.0.1:10113 fail_timeout=0;
    server 127.0.0.1:10114 fail_timeout=0;
    server 127.0.0.1:10115 fail_timeout=0;
    server 127.0.0.1:10116 fail_timeout=0;
    server 127.0.0.1:10117 fail_timeout=0;
    server 127.0.0.1:10118 fail_timeout=0;
    server 127.0.0.1:10119 fail_timeout=0;
    server 127.0.0.1:10120 fail_timeout=0;
    server 127.0.0.1:10121 fail_timeout=0;
    server 127.0.0.1:10122 fail_timeout=0;
    server 127.0.0.1:10123 fail_timeout=0;
    server 127.0.0.1:10124 fail_timeout=0;
    server 127.0.0.1:10125 fail_timeout=0;
    server 127.0.0.1:10126 fail_timeout=0;
    server 127.0.0.1:10127 fail_timeout=0;
    server 127.0.0.1:10128 fail_timeout=0;
    server 127.0.0.1:10129 fail_timeout=0;
    server 127.0.0.1:10130 fail_timeout=0;
    server 127.0.0.1:10131 fail_timeout=0;
    server 127.0.0.1:10132 fail_timeout=0;
    server 127.0.0.1:10133 fail_timeout=0;
    server 127.0.0.1:10134 fail_timeout=0;
    server 127.0.0.1:10135 fail_timeout=0;
    server 127.0.0.1:10136 fail_timeout=0;
    server 127.0.0.1:10137 fail_timeout=0;
    server 127.0.0.1:10138 fail_timeout=0;
    server 127.0.0.1:10139 fail_timeout=0;
    server 127.0.0.1:10140 fail_timeout=0;
    server 127.0.0.1:10141 fail_timeout=0;
    server 127.0.0.1:10142 fail_timeout=0;
    server 127.0.0.1:10143 fail_timeout=0;
    server 127.0.0.1:10144 fail_timeout=0;
    server 127.0.0.1:10145 fail_timeout=0;
    server 127.0.0.1:10146 fail_timeout=0;
    server 127.0.0.1:10147 fail_timeout=0;
    server 127.0.0.1:10148 fail_timeout=0;
    server 127.0.0.1:10149 fail_timeout=0;
    server 127.0.0.1:10150 fail_timeout=0;
    server 127.0.0.1:10151 fail_timeout=0;
    server 127.0.0.1:10152 fail_timeout=0;
    server 127.0.0.1:10153 fail_timeout=0;
    server 127.0.0.1:10154 fail_timeout=0;
    server 127.0.0.1:10155 fail_timeout=0;
    server 127.0.0.1:10156 fail_timeout=0;
    server 127.0.0.1:10157 fail_timeout=0;
    server 127.0.0.1:10158 fail_timeout=0;
    server 127.0.0.1:10159 fail_timeout=0;
    server 127.0.0.1:10160 fail_timeout=0;
    server 127.0.0.1:10161 fail_timeout=0;
    server 127.0.0.1:10162 fail_timeout=0;
    server 127.0.0.1:10163 fail_timeout=0;
    server 127.0.0.1:10164 fail_timeout=0;
    server 127.0.0.1:10165 fail_timeout=0;
    server 127.0.0.1:10166 fail_timeout=0;
    server 127.0.0.1:10167 fail_timeout=0;
    server 127.0.0.1:10168 fail_timeout=0;
    server 127.0.0.1:10169 fail_timeout=0;
    server 127.0.0.1:10170 fail_timeout=0;
    server 127.0.0.1:10171 fail_timeout=0;
    server 127.0.0.1:10172 fail_timeout=0;
    server 127.0.0.1:10173 fail_timeout=0;
    server 127.0.0.1:10174 fail_timeout=0;
    server 127.0.0.1:10175 fail_timeout=0;
    server 127.0.0.1:10176 fail_timeout=0;
    server 127.0.0.1:10177 fail_timeout=0;
    server 127.0.0.1:10178 fail_timeout=0;
    server 127.0.0.1:10179 fail_timeout=0;
    server 127.0.0.1:10180 fail_timeout=0;
    server 127.0.0.1:10181 fail_timeout=0;
    server 127.0.0.1:10182 fail_timeout=0;
    server 127.0.0.1:10183 fail_timeout=0;
    server 127.0.0.1:10184 fail_timeout=0;
    server 127.0.0.1:10185 fail_timeout=0;
    server 127.0.0.1:10186 fail_timeout=0;
    server 127.0.0.1:10187 fail_timeout=0;
    server 127.0.0.1:10188 fail_timeout=0;
    server 127.0.0.1:10189 fail_timeout=0;
    server 127.0.0.1:10190 fail_timeout=0;
    server 127.0.0.1:10191 fail_timeout=0;
    server 127.0.0.1:10192 fail_timeout=0;
    server 127.0.0.1:10193 fail_timeout=0;
    server 127.0.0.1:10194 fail_timeout=0;
    server 127.0.0.1:10195 fail_timeout=0;
    server 127.0.0.1:10196 fail_timeout=0;
    server 127.0.0.1:10197 fail_timeout=0;
    server 127.0.0.1:10198 fail_timeout=0;
    server 127.0.0.1:10199 fail_timeout=0;
}



server {
    listen 80;
    server_name sdk.user.gamex.mobile.youku.com;
    charset utf-8;

    set $x_remote_addr $http_x_real_ip;
    if ($x_remote_addr = "") {
        set $x_remote_addr $remote_addr;
    }
    location /static/ {
        alias /opt/app/python/m-game-platform/api/static/;

    }

    location / {
        proxy_pass          http://sdk_user_api;
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


#server {
#    listen       443;
#    server_name  sdk.user.gamex.mobile.youku.com;

#    ssl                  on;
#    ssl_certificate /opt/app/python/m-game-platform/api/conf/ca/33iq.crt;
#    ssl_certificate_key /opt/app/python/m-game-platform/api/conf/ca/33iq_nopass.key;

#    ssl_session_timeout  5m;

#    ssl_protocols  SSLv2 SSLv3 TLSv1;
#    ssl_ciphers  HIGH:!aNULL:!MD5;
#    ssl_prefer_server_ciphers   on;

#    location / {
#        proxy_pass          http://sdk_user_api;
#        proxy_connect_timeout 3;
#        proxy_send_timeout 3;
#        proxy_read_timeout 3;
#        proxy_redirect      default;
#        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
#        #proxy_set_header    X-Real-IP $x_remote_addr;
#        proxy_set_header    Host $http_host;
#        proxy_set_header    Range $http_range;
#    }
#}