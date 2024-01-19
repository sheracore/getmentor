# GetMentor
## install requirements
```commandline
install -r requirements.txt
```

## install ffmpeg to calculate video and voice duration
```commandline
sudo apt install ffmpeg
```

## Postgres
Change values in brackets to what you set in .env file for db name, user and password.
```commandline
sudo -u postgres psql
postgres=# CREATE DATABASE [your db name];
postgres=# CREATE USER [your db user] WITH PASSWORD [your db password];
postgres=# GRANT ALL PRIVILEGES ON DATABASE [your db name] TO [your db user];
postgres=# \q
```

## redis
```commandline
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis
```
* Install from Snapcraft
```commandline
sudo snap install redis
```

## celery
### development
```commandline
celery -A DJANGO_PROJECT worker -l INFO
celery -A DJANGO_PROJECT beat -l info -S django
```


### Production services
```commandline
Comming soon...
```