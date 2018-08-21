# NginxPythonFileupload
This is a program of file upload by web, base on nginx upload module and python tornado

# How to installation and configure in Ubuntu
apt-get install build-essential g++ gcc make 

cd /data

wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.39.tar.gz

tar -zxvf pcre-8.39.tar.gz

 

git clone -b 2.2 https://github.com/vkholodkov/nginx-upload-module

wget http://nginx.org/download/nginx-1.10.3.tar.gz
tar -zxvf nginx-1.10.3.tar.gz

cd nginx-1.10.3/

./configure --add-module=/data/nginx-upload-module --with-pcre=/data/pcre-8.39 --with-zlib=/data/zlib-1.2.11 --with-http_gzip_static_module --with-openssl=/data/openssl-1.0.2j --with-http_ssl_module 

make 

make install

