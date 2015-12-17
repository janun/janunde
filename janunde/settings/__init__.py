import sys
# use test settings if run by python manage.py test ...
if sys.argv[1:2] == ['test']:
    from .testing import *
else:
    from .dev import *
