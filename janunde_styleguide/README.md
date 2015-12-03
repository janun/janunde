# janun.de Styleguide
These are reusable styles developed for janun.de.

## The Styles
 The actual styles live in the subdir [styles](styles).
 Styles can define
  * sass code (in name_of_style.scss)
  * templates (in the subdir templates)
  * templatetags (in templatetags.py)
  * Documentation (in _doc.html)

Templatetags are most useful here:
This way the HTML of a component can be changed without the app using the component needing change.

## Dependencies
Still need to document this.

## Installation
1. add to INSTALLED_APPS in PROJECT_DIR/settings/base.py:
```python
  INSTALLED_APPS += ('janunde_styleguide',)
```

2. add to PROJECT_DIR/urls.py:
We only need to see the actual styleguide in development.
```python
if settings.DEBUG:
  urlpatterns.insert(0, url(r'^styleguide/', include('janunde_styleguide.urls')) )
```

3. add template path in PROJECT_DIR/settings/base.py:
```python
TEMPLATES = [{
  ...
  'DIRS': [
    ...
    os.path.join(BASE_DIR, 'janunde_styleguide', 'styles'),
    ...
  ]
}]
```

4. add static files finder in PROJECT_DIR/settings/base.py:
```python
STATICFILES_FINDERS = (
  ...
  'styles.finders.StyleFinder',
  ...
)
```
