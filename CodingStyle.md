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


#### template file naming
 - `_filename.html`  for those that are included in other templates
 - `__filename.html` for those that are extended upon from other templates


## Sass files
Should be commented using [SassDoc](http://sassdoc.com/)

Variables are normally written in lower case, with hyphens connecting names.


### class naming

#### BEM
Classes are named/organized using the BEM principle,
with the following naming style:
 - `block`                          for blocks
 - `block__element`                 for elements
 - `block--modifier`                for modifiers
 - `block--modifier@medium`         applies only for screen-width >= $medium
 - `block--modifier@until-medium`   applies only for screen-width <  $medium

#### namespace for js
Scripts should bind to extra classes that begin with `js-`
instead of using css classes.

### ordering of declarations in a selector
1. sass @imports
2. css declarations
  1. positioning
  2. box model
  3. typography
  4. visuals
  5. other
3. nested selectors

### vendor-prefixes
Do not prefix. It’s handled by autoprefixer automatically.
