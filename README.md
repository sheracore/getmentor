# GetMentor


For Postgres Database
Change values in brackets to what you set in .env file for db name, user and password.
```commandline
sudo -u postgres psql
postgres=# CREATE DATABASE [your db name];
postgres=# CREATE USER [your db user] WITH PASSWORD [your db password];
postgres=# ALTER ROLE [your db user] SET client_encoding TO 'utf8';
postgres=# ALTER ROLE [your db user] SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE [your db user] SET timezone TO 'UTC';
postgres=# GRANT ALL PRIVILEGES ON DATABASE [your db name] TO [your db user];
postgres=# \q
```
