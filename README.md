# Source for janun.de
This is the source of janun.de, the website for JANUN e.V.

It is based on [Django](http://djangoproject.com) and [Wagtail](http://wagtail.io).


## Development
To get a development environment, you can use a python virtualenv
and install the dependencies:

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
npm install
```

`npm install` installs all frontend dependencies including bower components
and runs gulp to compile assets.

You then need to create a postgres database:
```bash
sudo su postgres
createuser -P janunde
createdb -O janunde janunde_db
logout
```

And run the migrations:
```bash
python manage.py migrate
```


## Deployment
If you want to test code changes, you can deploy on heroku with a click of a button:
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)
