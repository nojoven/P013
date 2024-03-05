# P013
P13 2023

# STAYS
## STAYS is a web social media for people who like to tell and share their stories.

<!--
<<<<<<< HEAD
Ceci est pour une démo
Armagnac.
=======


+
+Cd vers répertoire où il y a manage.py
+
-->

There are two ways to install Stays: manually or automatically.
<!--
Scripter tout ça

-->
### Automated installation

Start a terminal,go to your typical development working directory, and copy/paste the following lines:

```bash

# Repository definition:

# URL originale:
repo_name="P013"
git_url="github.com/nojoven/${repo_name}.git"
 
# URL de mon clone:
repo_name="cjo_p013"
git_url="github.com:pchg/${repo_name}.git"

# Reference branch:
git_branch="develop"
git_branch="modifs_pierre"




# Clone the Stays' repository (depth 1 is useful for persons with poor Internet connection, since the complete .git is quite heavy (185M, as of 2024_03_03__23_48_25)):
git clone https://${git_url} --depth 

# Get to the reference branch (useful during debug phase):
git checkout "${git_branch}"

# Move to project directory and to subdirectory where manage.py is located:
cd ${repo_name}/stays/

# Make a Python virtual environment, and activate it:
if [[ ! -d .venv ]]; then 
  echo "Creation of Python virtual environment..."
  python3 -m venv .venv
  echo "Install required Python packages into the virtual environment.."
  pip install ../requirements.txt
fi
source .venv/bin/activate

# Get environment variables:
source .env


# python manage.py collection_static
python manage.py collectstatic
# __________***_JEANSUILA_***__________

python manage.py make migrations
python manage.py migrate
python manage.py runserver
```


## Database user

Create postgresql user with the name "staydmin"

```
GRANT ALL PRIVILEGES ON DATABASE defaultdb TO staydmin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO staydmin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO staydmin;
```


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
   - ```python manage.py migrate```  


## Populate cities_light

``` python manage.py cities_light```

## Set the root of static files

```python manage.py collectstatic```

## Start the project

### Run the command

   - ```cd P013/stays```
   - ```poetry shell```
   - ```python manage.py runserver 8001```
   - ```python manage.py migrate```

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

<!--
+
+Cd vers répertoire où il y a manage.py
+
-->
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

