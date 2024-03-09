# P013
P13 2023

# STAYS
## STAYS is a web social media for people who like to tell and share their stories.

## Environment variables
- in staiys/stays rename the *env* file to ***.env***
- add the missing values

## Data storages
You need to install Postgresql and Redis


### Database user
Create postgresql user with the name "staydmin"
```
GRANT ALL PRIVILEGES ON DATABASE defaultdb TO staydmin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO staydmin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO staydmin;
```



## Install this project manually:
   - Clone the repository
   - Checkout to branch main
   - ```cd stays``` 
   - ```python -m venv .venv```
   - ```source .venv/bin/activate```
   - ```pip install -r requirements.txt```

## Configurations
   - The settings require a .env file
   - Add the missing values

## Migrations
   - ```python manage.py makemigrations users```
   - ```python manage.py migrate users```
   - ```python manage.py makemigrations core```
   - ```python manage.py migrate core```
   - ```python manage.py makemigrations locations```
   - ```python manage.py migrate locations```
   - ```python manage.py migrate```  


## Populate cities_light
``` python manage.py cities_light```

## Set the root of static files
```python manage.py collectstatic```

## Start the project
### Run the command
   - ```cd P013/stays```
   - ```source .venv/bin/activate```
   - ```python manage.py runserver```
   - ```python manage.py migrate```

### Create an administrator
   - In another terminal ```python manage.py createsuperuser```
   - Define the email and the password of your superuser
   - You can connect at ```localhost:5000/admin```


### Run tests:
```python manage.py runtests```

## Credits:
   - https://www.drlinkcheck.com/blog/free-http-error-images
   - https://freefrontend.com/403-forbidden-html-templates
   - https://freefrontend.com/500-error-page-html-templates
   - A Pen created on CodePen.io. Original URL: [https://codepen.io/shubniggurath/pen/NLYzLj](https://codepen.io/shubniggurath/pen/NLYzLj).
   - [https://codepen.io/jsonyeung/pen/ZMxdPg](https://codepen.io/jsonyeung/pen/ZMxdPg)
