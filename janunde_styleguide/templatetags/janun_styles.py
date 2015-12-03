#from django import template
#register = template.Library()
from janunde_styleguide.tag_library import JanunTagLibrary
register = JanunTagLibrary()

# TODO: automate this
from janunde_styleguide.styles.components.panels import templatetags
from janunde_styleguide.styles.patterns.colors import templatetags
from janunde_styleguide.styles.components.header import templatetags
from janunde_styleguide.styles.components.teaser import templatetags
from janunde_styleguide.styles.components.search import templatetags
from janunde_styleguide.styles.components.navbar import templatetags
