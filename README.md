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
$ gunicorn manage:app
```

## Demo Application
For testing Demo Application is live on [Heroku](https://koshex.herokuapp.com)


## Sample Requests
1. For creating tiny url
```
$ curl --location --request POST 'https://koshex.herokuapp.com/tiny/create' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "https://www.google.com/search?channel=fs&client=ubuntu&q=access+inherited+class+value+in+python"
}'
```

2. For searching keywords 'python' in already shortened url/
```
$ curl --location --request GET 'https://koshex.herokuapp.com//tiny/search?key=python'
```

3. For Fetching metadata of stored url - pass shorten base_path of url to route.
```
$ curl --location --request GET 'https://koshex.herokuapp.com/tiny/y2agkcpj'
```

