docker run --name some-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=1234 -d mysql

mysql -u root -p
p: 1234

user database;
show tables;
drop table `table_name`