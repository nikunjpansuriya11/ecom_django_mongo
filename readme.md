# Ecommerce web for puma products

This project is for scraping data from the puma website and showing in created web with functionality of user authentication, show product list in the proper format and cart system, and many more.

## Installation

need to install requirements for this project in your env there for the below command needs to run.

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Setps for project setup

right now in this project, all my cred are use for testing.

```python
cd ecommerce

# first you need to change you database cred in setting file over here "ecommerce/ecommerce/settings.py" 
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'db name',
    }
}


# for migration use this commands
python manage.py makemigrations
python manage.py migrate

# for collect static files use this command
python manage.py collectstatic

# for create super user creation
python manage.py createsuperuser

# for run website
python manage.py runserver
```

## For Start Scrapping there is two way 

1. first way using management command you can get scrape product.
```python
#fisrt scrapper is for scrape url from puma web and store in db and there for command
python manage.py scrapper1.py

#second scrapper is for scrape producat data from puma web and store in db and there for command
python manage.py scrapper2.py

#final scrapper is for scrape producat description from puma web and store in db and there for command
python manage.py scrapper3.py
```

2. second way using crontab you can get scrape product.
```python
# there is task folder in project dir in that three .sh file for cron 

# now, you need to create cron command for all of three .sh file and formate is shows below
52 14 * * * /bin/bash /your/sh/file/path >> /your/loagger/path 2>&1

#now enter command cmd to below
crontab -e

now past all three command in line in terminal
now save using Ctrl+S and exit usign Ctrl+C

#there add all three cron on your system as your given time and that's on that time.
```

finally i have attached postman collection for ecom web is here
https://api.postman.com/collections/16654720-493c398e-ba33-474a-bfb3-55f73c39bb61?access_key=PMAT-01GM5DSKYS0MVW4ZBJSAA9K7GR
this link you need to import in your postman collection.