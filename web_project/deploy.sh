#!/bin/bash
if [ ! -d "/opt/downloads" ];then
 mkdir /opt/downloads
fi

echo '[start install pcre!]'
cd /opt/downloads/
wget -O pcre-8.32.tar.gz http://sourceforge.net/projects/pcre/files/pcre/8.32/pcre-8.32.tar.gz/download
tar zxvf pcre-8.32.tar.gz
cd pcre-8.32
./configure
make
make install
cd /lib64
ln -s libpcre.so.0.0.1 libpcre.so.1
ldconfig

echo '[start install zlib!]'
cd /opt/downloads/
wget http://prdownloads.sourceforge.net/libpng/zlib-1.2.7.tar.gz?download
tar zxvf zlib-1.2.7.tar.gz
cd zlib-1.2.7
./configure --prefix=/usr/local
make
make install

echo '[start install nginx-1.0.4!]'
cd /opt/downloads/
wget http://nginx.org/download/nginx-1.0.4.tar.gz
tar zxvf nginx-1.0.4.tar.gz
cd nginx-1.0.4
./configure \
--prefix=/opt/nginx
make
make install

echo '[start install python!]'
cd /opt/downloads/
wget http://www.python.org/ftp/python/2.7.2/Python-2.7.2.tgz
tar zxf Python-2.7.2.tgz
cd Python-2.7.2
./configure --prefix=/opt/python2.7
make
make install
export PATH=/opt/python2.7/bin:$PATH
echo "export PATH=/opt/python2.7/bin:\$PATH" > /etc/profile.d/python.sh

echo "[setup setuptools from ]"
cd /opt/downloads/
wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz#md5=7df2a529a074f613b509fb44feefe74e
tar zxvf setuptools-0.6c11.tar.gz
cd setuptools-0.6c11
/opt/python2.7/bin/python setup.py install

echo "[install supervisord]"
cd /opt/downloads/
wget https://github.com/Supervisor/supervisor/archive/3.0a10.tar.gz --no-check-certificate
tar zxvf supervisor-3.0a10.tar.gz
cd supervisor-3.0a10
/opt/python2.7/bin/python setup.py install

echo "[install ldap]"
yum install openldap24-libs  openldap

if [ ! -d "/opt/downloads" ];then
mkdir /opt/downloads
fi
echo "[setup git]"
cd /opt/downloads/
wget http://git-core.googlecode.com/files/git-1.8.1.1.tar.gz
tar zxvf git-1.8.1.1.tar.gz
cd git-1.8.1.1
./configure --prefix=/usr/local
make
make install

#echo "10.10.0.5 gforge.1verge.net" >> /etc/hosts
echo "[Clone Project]"
if [ ! -d "/opt/app/python" ];then
mkdir -p /opt/app/python
fi
cd /opt/app/python
git clone ssh://lidongdong@gforge.1verge.net/gitroot/m-app-exchange m-app-game

echo "make logs dir"
mkdir -p /opt/logs/nginx/access
mkdir -p /opt/logs/nginx/error
mkdir -p /opt/logs/nginx/statis
mkdir -p /opt/logs/tornado
mkdir -p /opt/logs/tornado/game
mkdir -p /opt/run

echo "start app"
cd /opt/app/python/m-app-game/app
chmod u+x restart.sh
./restart.sh

echo "start api"
cd /opt/app/python/m-app-game/api
chmod u+x tornado.sh
./tornado.sh start

echo "start nginx"
rm -rf /opt/nginx/conf/nginx.conf
ln -s /opt/app/python/m-app-game/base/conf/nginx.conf /opt/nginx/conf/nginx.conf
ln -s /opt/app/python/m-game-platform/app/conf/test.app.gamex.mobile.youku.com /opt/nginx/conf/test.app.gamex.mobile.youku.com
ln -s /opt/app/python/m-game-platform/api/conf/test.api.gamex.mobile.youku.com /opt/nginx/conf/test.api.gamex.mobile.youku.com
ldconfig
/opt/nginx/sbin/nginx -c /opt/nginx/conf/nginx.conf