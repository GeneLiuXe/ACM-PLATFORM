# ACM-PLATFORM
A small website is used for the management of ACM training problem library, competitions, teams, completed problems with solution.

# How to Run
1. Install support libraries needed for this project (Tornado 4.5.3+, pymsql 0.9.2+, python 3.7+, mysql 8.0.16+)
2. Import the sql data into mysql, modify the mysql connection parameters in config.py, and run server.py.

# Details of Installation

Taking Ubuntu 18.04 for example.

> python3

```shell
sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip
pip3 install package_name
```
> pymysql

```shell
python3 -m pip install PyMySQL
```

> tornado

```shell
sudo apt-get install python3-tornado
```

> mysql

Installation of mysql 8.0+.

```shell
sudo wget https://dev.mysql.com/get/mysql-apt-config_0.8.14-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.14-1_all.deb
sudo apt-get update
sudo apt-get install mysql-server
mysql_secure_installation
mysql -u root -p # login to MySQL Database
```
Create a MySQL remote user.

```shell
mysql -u root -p
CREATE USER 'root'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;
```
Enable MySQL remote access.

```shell
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
# change the "bind-address = 127.0.0.1" into "bind-address = 0.0.0.0"
sudo systemctl restart mysql.service
```

[Reference link](https://www.fosstechnix.com/install-mysql-8-on-ubuntu/)

> Run

Install Screen and run the project in it.

```shell
sudo apt-get install screen
screen
python3 server.py
```

# Web Portal
![Image of Web](https://github.com/GeneLiuXe/ACM-PLATFORM/blob/master/Figures/Web%20portal.png)

# Main Page
![Image of Web](https://github.com/GeneLiuXe/ACM-PLATFORM/blob/master/Figures/Main%20Page.png)

# Problem Library
![Image of Web](https://github.com/GeneLiuXe/ACM-PLATFORM/blob/master/Figures/Problem%20Library.png)

# Contest
![Image of Web](https://github.com/GeneLiuXe/ACM-PLATFORM/blob/master/Figures/Contest.png)

# User
![Image of Web](https://github.com/GeneLiuXe/ACM-PLATFORM/blob/master/Figures/User.png)

# More Details
If you want to know more information, you could consult for the "ACM-PLATFORM Report.pdf" in this project.
