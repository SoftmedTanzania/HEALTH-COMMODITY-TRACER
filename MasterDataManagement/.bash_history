sudo su
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
echo "export WORKON_HOME=~/Env" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc
mkvirtualenv HealthCommodityTracer
clear
workon HealthCommodityTracer
deactivate
sudo apt-get install python3-dev
sudo -H pip3 install uwsgi
sudo mkdir -p /etc/uwsgi/sites
sudo nano /etc/uwsgi/sites/healthcommoditytracer.ini
sudo nano /etc/systemd/system/uwsgi.service
sudo apt-get install nginx
clear
sudo nano /etc/nginx/sites-available/healthcommoditytracer
sudo ln -s /etc/nginx/sites-available/healthcommoditytracer /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo apt-get update
sudo apt-get install mysql-server
sudo ufw allow mysql
systemctl enable mysql
/usr/bin/mysql -u root -p
clear
mysql -u root -psudo apt-get remove --purge mysql-server mysql-client mysql-common -y
sudo apt-get remove --purge mysql-server mysql-client mysql-common -y
sudo apt-get autoremove -y
sudo apt-get autoclean
rm -rf /etc/mysql
sudo find / -iname 'mysql*' -exec rm -rf {} \;
clear
sudo apt-get update
sudo apt-get install mysql-server
sudo ufw allow mysql
systemctl start mysql
Wewewawa90
systemctl enable mysql
/usr/bin/mysql -u root -p
clear
sudo apt-get update
sudo apt-get install python3-pip
sudo -H pip3 install --upgrade pip
pip3 install virtualenv virtualenvwrapper
sudo su
sudo su 
mysql -u root -p
Mysql2019>
mysql -u root -p
sudo mysql
clear
mysql -u root -p
clear
workon healthcommoditytracer
ls
cd Env
ls
workon HealthCommodityTracer
cd healthcommoditytracer
ls
clear
cd Hea
cd HealthCommodityTracer/
ls
workon HealthCommodityTracer
ls
cd healthcommoditytracer/
ls
python3 manage.py makemigrations 
ls
pip3 install -r requirements.txt 
sudo apt-get install python3.6-dev libmysqlclient-dev
pip3 install --upgrade setuptools
pip3 install -r requirements.txt 
python3 manage.py makemigrations
pip3 install django-bootstrap4
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py createsuperuser
sudo su
clear
cd /home/
ls
sudo service uwsgi restart
systemctl daemon-reload
sudo service uwsgi restart
sudo service nginx restart
sudo systemctl enable nginx
sudo systemctl enable uwsgi
sudo tail -F /var/log/nginx/error.log
cd /etc/nginx/
ls
cd sites-available/
ls
sudo nano default 
rm -r default 
ls
sudo su
sudo tail -F /var/log/nginx/error.log
cd /run/uwsgi/
ls
sudo nano healthcommoditytracer.sock 
clear
cd /etc/uwsgi/
cd sites
ls
sudo nano healthcommoditytracer.ini 
cd /run/uwsgi/
ls
sudo su
clear
mkvirtualenv healthcommoditytracer
workon healthcommoditytracer
cd healthcommoditytracer
ls
cd home
ls
cd danny
ls
cd d
deactivate
srvice uwsgi restart
sudo service uwsgi restart
sudo service nginx restart
clear
workon healthcommoditytracer
ls -la
cd healthcommoditytracer/
ls
pip3 install -r requirements.txt 
python3 manage.py makemigrations
pip3 install django-bootstrap4
python3 manage.py makemigrations
python3 manage.py runserver
python3 manage.py runserver 0.0.0.0:8000
sudo lsof -t -i tcp:8000 | xargs kill -9
python3 manage.py runserver 0.0.0.0:8000
clear
sudo service nginx restarrt
sudo service nginx restart
sudo service uwsgi restart
tail - F /var/log/nginx/error.log 
tail -F /var/log/nginx/error.log 
deactivate
tail -F /var/log/nginx/error.log 
sudo tail -F /var/log/nginx/error.log 
cd ..
clear
workon healthcommoditytracer
cd healthcommoditytracer/
ls
‰ˆdeactivate
deactivate
rmkvirtualenv healthcommoditytracer
mkvirtualenv HealthCommodityTrcaer
pip install -r requirements.txt 
pip3 install django-bootstrap4
cd home
deactiavte
deactivate
clear cd //
cd //
clear
ls
ls -la
sudo ln -s /etc/nginx/sites-available/healthcommoditytracer /etc/nginx/sites-enabled
cd ..
cd sites-enabled/
ls
sudo su
clear
cd ..
sudo tail -F /var/log/nginx/error.log 
sudo reboot
cd /etc/uwsgi/sites/
ls
sudo nano healthcommoditytracer.ini 
sudo nano /etc/systemd/system/uwsgi.service 
sudo /etc/nginx/sites-available/
cd /etc/nginx/sites-available/
ls
sudo nano healthcommoditytracer 
nano HealthCommodityTracer
sudo nano HealthCommodityTracer
cd ..
cd sites-enabled/
ls
sudo su
ls
cd ..
ls
cd Env
ls
cd ..
ls
clear
sudo su
workon HealthCommodityTracer
ls
cd danny
ls
workon HealthCommodityTracer
cd Env
ls
rmvirtualenv HealthCommodityTrcaer
ls
mkvirtualenv HealthCommodityTracer
pip3 install -r requirements.txt
cd HealthCommodityTracer/
pip3 install -r requirements.txt
ls
deactivate
clear
ls
cd ..
clear
ls
workon HealthCommodityTracer
ls
cd HealthCommodityTracer/
ls
pip3 install -r requirements.txt
pip3 install django-bootstrap4
sudo su
clear
suod apt-get update
sudo apt-get update
sudo apt-get install phpmyadmin
sudo sy
sudo su
clear
sudo su
clear
ls
rm -r HealthCommodityTracer/
mysql - root -p
cler
clear
mysql -u root -p
clear
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
clear
python3 manage.py collectstatic
python3 manage.py craetesuperuser
python3 manage.py createsuperuser
sudo service uwsgi restart
sudo service nginx restart
mysql -u root -p
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations --merge
pip3 install django_excel
python3 manage.py makemigrations --merge
python3 manage.py makemigrations
python3 manage.py migrate
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate --fake
python3 manage.py runserver
sudo service uwsgi restart
sudo service nginx restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx  restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
mysql -u root -p
clear
sudo service uwsgi restart
service nginx restart
mysql -u root -p
ls
rm -r HealthCommodityTracer/
ls 
mysql -u root -p
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
pip3 install django-cors-headers
python3 manage.py makemigrations
pip3 install django-mptt
python3 manage.py makemigrations
clear
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
clear
python3 manage.py createsuperuser
sudo service uwsgi restart
service nginx restart
ls
rm HealthCommodityTracer/
rm -r HealthCommodityTracer/
ls
mysql -u root -p
clear
mysql -u root -p
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigration
python3 manage.py makemigrations
mysql -u root -p
clear
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py createsuperuser
sudo service uwsgi restart
service nginx restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
sudo service uwsgi restart
service nginx restart
sudo service uwsgi restart
service nginx restart
sudo service uwsgi rstart
sudo service uwsgi restart
sudo service nginx restart
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
systemctl restart mysql.service
clear
mysql -u root -p
clear
sudo nano etc/mysql/mysql.conf.d/mysqld.cnf
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
systemctl restart mysql
mysql -u root -p
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py makemigrations 
python3 manage.py migrate
clear
python3 manage.py makemigrations 
mysql -u root -p
sudo service uwsgi restart
service nginx restart
tail -f /var/log.nginx/error.log
sudo tail -F /var/log/nginx/error.log
clear
mysql -u root -p
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py createsuperuser
clear
mysql -u root -p 
python3 manage.py makemigrations
python3 manage.py migrate
sudo tail -F /var/log/nginx/error.log
clear
sudo service uwsgi restart
service nginx restart
mysql -u root -p
sudo service uwsgi restart
service nginx restart
sudo service uwsgi restart
Wewewawa90
sudo service uwsgi restart
service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
Service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
Wewewawa90
sudo service nginx restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py collectstatic
sudos ervice uwsgi restart
sudo service uwsgi restart
sudo servicenginx  restart
clear
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
clear
sudo service uwsgi restart
sudo service nginx restart
sudo service nginx  restart
sudo service uwsgi restart
sudo service uwsgi restart
sudo service nginx  restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py collectstatic
sudo service uwsgi restart
sudo service nginx restart
clear
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx  restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
pips install django-fcm
pip3 install django-fcm
python3 manage.py makemigrations
clear
python3 manage.py makemigrations
clear
python3 manage.py makemigrations
clear
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigartions
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
clear
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
clear
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
clear
adduser ilakoze
sudo su
sudo service uwsgi restart
sudo service nginx restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
mysql -u root -p
clear
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
clear
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
sudo service uwsgi restart
sudo service nginx restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
clear
cd /etc/uwsgi/sites
ls
sudo nano HealthCommodityTracer.ini 
ls
sudo nano HealthCommodityTracer.ini 
sudo nano /etc/systemd/system/uwsgi.service
sudo nano /etc/nginx/sites-available/HealthCommodityTracer 
sudo service uwsgi restart
sudo service nginx restart
mysql -u root -p
sudo apt update
sudo apt install phpmyadmin php-mbstring php-gettext
sudo phpenmod mbstring
sudo systemctl restart apache2
sudo apt install phpmyadmin php-mbstring php-gettext
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
sudos ervice uwsgi restart
sudo service uwsgi restart
sudo service nginx restart
cd /etc/nginx/sites-available/
ls -la
cd /etc/nginx/sites-enabled
ls -la
cd /etc/nginx/sites-available/
ls -la
sudo nano HealthCommodityTracer 
clear
ls -la
sudo nanon HealthCommodityTracer 
sudo nano HealthCommodityTracer 
cd /etc/uwsgi/
ls -la
cd sites/
ls -la
sudo nano HealthCommodityTracer.ini 
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
mysql -u root -p
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
mysql -u root -p 
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
mysql -u root -p
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
deactivate
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
clear
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.pymigrate
python3 manage.p ymigrate
python3 manage.py migrate
sud service uwsgi restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
tail -F
tail -F /var/log/nginx/error.log
sudo tail -F /var/log/nginx/error.log
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py runserver
sudo service  nginx stop
python3 manage.py runserver
sudo lsof -t -i tcp:8000 | xargs kill -9
python3 manage.py runserver
sudo service nginx restart
sudo service uwsgi stop
sudo service nginx  stop
python3 manage.py runserver
sudo lsof -t -i tcp:8000 | xargs kill -9
python3 manage.py runserver
sudo lsof -t -i tcp:8000 | xargs kill -9
python3 manage.py runserver 0.0.0.0:8000
sudo service uwsgi start
sudo service nginx  start
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
clear
mysql -u root -p
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
mysql -u root -p
clear
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
mysql -u root -p
sudo service uwsgi restart
sudo service nginx restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
python3 manage.py migrate
sudo service uwsi restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
sudo service nginx restart
mysqldump -u root -p HealthCommodityTracer > new_dump.sql
ls -la
rm -rf HealthCommodityTracer-backup-2019-09-09.sql 
clear
ls -la
scp danny@173.255.220.51:new_dump.sql ~/Desktop/
scp danny@173.255.220.51:new_dump.sql
scp danny@173.255.220.51:new_dump.sql ~/Desktop/
scp danny@173.255.220.51:new_dump.sql ~/Desktop/HTC-backup
scp danny@173.255.220.51:new_dump.sql ~/Desktop
clear
scp danny@173.255.220.51:new_dump.sql ~/Desktop/
scp danny@173.255.220.51:new_dump.sql ~/Desktop
scp danny@173.255.220.51:new_dump.sql 
scp danny@173.255.220.51:new_dump.sql /
scp danny@173.255.220.51:new_dump.sql >  ~/Desktop/
scp danny@173.255.220.51:new_dump.sql >  ~/Desktop
mysql -u root -p
sudo service uwsgi restart
sudo service nginx  restart
sudo service uwsgi restart
sudo service nginx restart
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py migrate
clear
pip3 install django-background-tasks
python3 manage.py migrate
clear
python3 manage.py migrate 
clear
python3 manage.py makemigrations
clear
pip3 uninstall django-background-tasks
pip3 install django-background-tasks
python3 manage.py migrate 
python3 manage.py makemigrations 
python3 manage.py migrate --fake
clear
python3 manage.py migrate --fake
clear
python manage.py schemamigration background-task --auto
python3 manage.py syncdb
mysql -u phpmyadmin -p
mysql -u root -p
clear
python3 manage.py migrate
workon HealthCommodityTracer
cd HealthCommodityTracer/
python3 manage.py makemigrations
clear
python3 manage.py migrate
clea
python3 manage.py showmigrations
clear
python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
udo service uwsgi restart
sudo service uwsgi restart
sudo service nginx restart
clear
crontab -l
clear
cd HealthCommodityTracer/
sudo nano cronjob.sh 
clear
grep "cronjob.sh" /home/danny/HealthCommodityTracer/
grep "cronjob.sh" /home/danny/HealthCommodityTracer/cronjob.sh 
sudo nano /var/log/syslog
sudo service uwsgi restart
sudo service nginx restart
sudo service uwsgi restart
