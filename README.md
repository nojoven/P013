# P013
P13 2023

# STAYS
## STAYS is a web social media for people who like to tell and share their stories.


## Install this project manually:
   - Clone the repository
   - Checkout to branch develop
   - ```cd stays/stays``` to open the file of the  pyproject.toml
   - ```python -m venv .venv```
   - ```source .venv/bin/activate```
   - ```pip install -r requirements.txt```
   - Install redis
   - Install Postgresql 15

## Configurations
   - Rename conf.js to confs.js
   - Add the missing values

## Migrations
   - ```python manage.py makemigrations users```
   - ```python manage.py migrate users```
   - ```python manage.py makemigrations core```
   - ```python manage.py migrate core```
   - ```python manage.py makemigrations locations```
   - ```python manage.py migrate locations```
   - ```python manage.py migrate```  (one last time)


## Populate cities_light
``` python manage.py cities_light```

## Set the root of static files
```python manage.py collectstatic```

## Start the project
### Run the command
   - ```cd P013/stays```
   - ```poetry shell```
   - ```python manage.py runserver 8001```

### Create an administrator
   - In another terminal ```python manage.py createsuperuser```
   - You can connect at ```localhost:5000/admin```

### Create a publication

### Configure the Queue manager
   - ```python manage.py qcluster```
   - Add these lines to pyproject.toml (or tox.ini ?):
      [Unit]
      Description=Django-Q cluster for My Project
      After=network.target

      [Service]
      User=myuser
      Group=www-data
      WorkingDirectory=/path/to/myproject
      ExecStart=/path/to/myenv/bin/python manage.py qcluster
      Restart=always

      [Install]
      WantedBy=multi-user.target

### Automated installation
```python manage.py setupstays```

### Run tests:
```python manage.py runtests```

#### Install mailpit
   - https://github.com/axllent/mailpit/releases/tag/v1.13.1

   - Start it manually from your terminal

   - Example of log ```INFO[2024/02/04 15:31:50] [http] accessible via http://localhost:8025/```


## Credits:
   - https://www.drlinkcheck.com/blog/free-http-error-images
   - https://freefrontend.com/403-forbidden-html-templates
   - https://freefrontend.com/500-error-page-html-templates
   - A Pen created on CodePen.io. Original URL: [https://codepen.io/shubniggurath/pen/NLYzLj](https://codepen.io/shubniggurath/pen/NLYzLj).
   - [https://codepen.io/jsonyeung/pen/ZMxdPg](https://codepen.io/jsonyeung/pen/ZMxdPg)
