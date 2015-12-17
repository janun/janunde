from .base import *

# make things faster
DEBUG=False
SECRET_KEY="blablabla"

# use extra database for manual testing
# manage.py test will create in memory db regardless
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'janunde_test_db.sqlite3',
}
