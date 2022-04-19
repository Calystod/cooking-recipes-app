# cooking-memory
## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)
### General Info
***
This project allows to save recipes
## Technologies
***
A list of technologies used within the project:
* [Flask Login](https://flask-login.readthedocs.io/en/latest/)
## Installation
***
For the first installation, you need to install:
* [Direnv](https://direnv.net/)
* [Virtualenv](https://virtualenv.pypa.io/en/latest/)

Add a file .envrc with the environment variable:
```
export FLASK_APP=main.py
export SECRET_KEY=@SECRET_KEY@
export PASSWORD_ADMIN=@PASSWORD_AMIN@
export EMAIL_ADMIN=me@email.test
export NAME_ADMIN=Admin
export FLASK_ENV=development
export FLASK_DEBUG=1
DEBUG_TB_INTERCEPT_REDIRECTS=0
DB_PASSWORD=@DB_PASSWORD@
DB_NAME=@DB_NAME@
DB_SERVER=@DB_SERVER@
DB_USER=@DB_USER@
```

```
$ direnv allow .
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ py scripts/install.py
#$ python
#$ >> from main import db, create_app
#$ >> db.create_all(app=create_app())
#$ >> exit()
$ python -m flask run
```

Go on http://127.0.0.1:5000/

