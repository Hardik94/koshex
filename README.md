# Koshex-App
Application for shortening the URL

## Steps to run Application

### 1. Create the New Database in postgresSQL
```
$ create database DBNAME;
```
and setup DB-url for accessing database for application
```
$ export DATABASE_URL=postgresql+psycopg2://{user}:{pass}@{DB_URL}/{DBNAME}
```
replace username, password, DB_URL, DBNAME with your Local Environment Config.

### 2. Install Dependencies for Application
Go to Project Folder
```
$ sudo pip3 install -r requirements.txt
```

### 3. Create Predefined tables for Application
```
$ python3 manage.py db init
$ python3 manage.py create_db
$ python3 manage.py db migrate
```

### 4. Run Application
```
$ python3 manage.py gunicorn
```

