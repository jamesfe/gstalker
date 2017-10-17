sudo yum -y install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs
sudo service postgresql initdb
sudo vim /var/lib/pgsql9/data/pg_hba.conf
# modify a line to: local/all/all/trust
# start service
sudo service postgresql start

sudo yum install git
cd ~
git clone https://github.com/jamesfe/gstalker.git
cd gstalker
sudo yum -y install python36
python3 -m venv --without-pip localenv
python3 -m pip install -r requirements.txt
mkdir config
vim config/config.json
source ./localenv/bin/activate
