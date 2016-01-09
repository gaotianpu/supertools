#Mac+Nginx+PHP+MySQL
##Nginx
1. nginx -v 

2. nginx启动、停止、重启
sudo nginx -s start
sudo nginx -s stop
sudo nginx -s reload

3. sudo nginx -t 
sudo vim /opt/local/etc/nginx/nginx.conf
sudo vim /opt/local/etc/nginx/conf.d/

4. log
tail /opt/local/var/log/nginx/error.log
tail /opt/local/var/log/nginx/access.log

5. www
/opt/local/www/plants

##php
1.	php --ini
/usr/local/etc/php/5.5/php.ini

2.	sudo find / -name php-fpm.conf
/private/etc/php-fpm.conf
/usr/local/etc/php/5.5/php-fpm.conf
but which one is the current config file ?

3. "Primary script unknown" while reading response header from upstream
原来：fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
修改后：fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;


##wordpress
cp -R wordpress  /opt/local/www/
rm -fR /opt/local/www/wordpress/


##projects
1. rsync
rsync -av ./  --exclude=*.bak /opt/local/www/plants
rsync -av ./  --exclude-from=excludefiles.txt   /opt/local/www/plants

2. auto run rsync script on sublime text 3's build system ?
cd /Users/gaotianpu/Library/Application\ Support/Sublime\ Text\ 3/Packages/User

#linux 文件权限
1. -rw-r--r--  644





