from django import template
register = template.Library()

@register.filter()
def cut(value, arg):
    return value.replace(arg, '')

@register.filter()
def prettyurl(value):
    return value.replace("http://", "").replace("https://", "").replace("www.", "")
