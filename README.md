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
bower install
```


## Deployment
Easy deployment to heroku is prepared.
We are using a second nodejs buildpack in addition to the python buildpack
for npm and bower dependencies.

```bash
heroku create
heroku buildpacks:add --index 1 heroku/nodejs
git push heroku master
heroku config:set SECRET_KEY=blablabla
heroku ps:scale web=1
heroku open
```


## Apps

### janunde_styleguide
This should be a living styleguide.
I hope I can use the app in other janun projects,
so we can have consistent UX there, too.

### home
The startpage

### search
wagtail app for searching
