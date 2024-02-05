# P013
P13 2023

# STAYS
## STAYS is a web social media for people who like to tell and share their stories.


## Install this project: 
   - Clone the repository
   - Checkout to branch develop
   - ```cd stays/stays``` to open the file of the  pyproject.toml
   - ```poetry install``` (or ```pip install -r requirements.txt``` )
   - ````python manage.py makemigrations```
   - ````python manage.py migrate```

## Start the project
### Run the command     ```poetry shell```
```python manage.py runserver```


### Install the Queue manager
```python manage.py qcluster```

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


sudo systemctl start myproject-qcluster
sudo systemctl enable myproject-qcluster

### Run tests:
```python -m pytest --import-mode importlib```




#### Install mailpit
https://github.com/axllent/mailpit/releases/tag/v1.13.1

start it 
INFO[2024/02/04 15:31:50] [http] accessible via http://localhost:8025/


credits
https://www.drlinkcheck.com/blog/free-http-error-images
https://freefrontend.com/403-forbidden-html-templates
https://freefrontend.com/500-error-page-html-templates
# 500 Error

A Pen created on CodePen.io. Original URL: [https://codepen.io/shubniggurath/pen/NLYzLj](https://codepen.io/shubniggurath/pen/NLYzLj).
[https://codepen.io/jsonyeung/pen/ZMxdPg](https://codepen.io/jsonyeung/pen/ZMxdPg)
