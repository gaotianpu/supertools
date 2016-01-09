#mysql常见问题
Q:ERROR 2003 (HY000): Can't connect to MySQL server on '192.168.1.111' (61)
A: 找到my.cnf，把#bind-address  = 127.0.0.1 这行给注释掉！

Q:ERROR 1130 (HY000): Host '192.168.1.100' is not allowed to connect to this MySQL server
A:GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'yourpassword' WITH GRANT OPTION;
