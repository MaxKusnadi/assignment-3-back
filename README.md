# Assignment 3 Backend

## Setup
```
$ mkvirtualenv a3 
$ pip install --editable .
$ export FLASK_APP=a3/app.py
$ flask init_db
$ flask run
```

## Setup v.2
- Install virtualenv
- Install [https://github.com/kennethreitz/autoenv](autoenv)
- Activate virtualenv
- Install all packages
`pip install -r requirements.txt`

### Running app
`python run.py`

### Running test cases with coverage
`. start_test.sh`

### Database
- Change your database URL in `config.py`
- Init DB
`python manage.py db init`
- Migrate DB
`python manage.py db migrate`
- Upgrade DB
`python manage.py db upgrade`
