# Coding Style

## Human Language
The language of variables, classes and so on is English.
Comments should be in English, too.
User facing strings are in German,
as in the moment i18n seems to be too much work.


## Indentation
Indentation is defined in `.editorconfig`,
which can be used by many editors.
Python files have 4 spaces indentation,
(almost) all other files have a 2 space indentation.


## Python files
* have 4 spaces indentation,
* should follow PEP8, which should be checked using:
    ```
    flake8 --exclude venv **/*.py
    ```

### Python Imports
Should be ordered by `isort`,
for which settings are also in `.editorconfig`.

### Python Variable Names
Use underscores, not camelCase, for variable, function and method names.

### Python Django templates
In Django template code, put one (and only one) space
between the curly brackets and the tag contents.


## Sass files
Should be commented using [SassDoc](http://sassdoc.com/)

Variables are normally written in lower case, with hyphens connecting names.
