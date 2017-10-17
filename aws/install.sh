sudo yum -y install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs
sudo service postgresql initdb
sudo vim /var/lib/pgsql9/data/pg_hba.conf
# modify a line to: local/all/all/trust
# start service
sudo service postgresql start
