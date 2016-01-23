from django import template
register = template.Library()

from wagtail.wagtailimages.shortcuts import get_rendition_or_not_found
from wagtail.wagtailimages.models import Filter


@register.filter()
def srcset(image, filter_specs):
    """generate a list of image renditions suitable for html5 srcset
    usage:
        srcset="{{ image|srcset:'width-320|jpg width-640|jpg' }}"
    """
    sources = []
    for filter_spec in filter_specs.split(' '):
        rendition = get_rendition_or_not_found(image, filter_spec)
        sources.append( "%s %sw" % (rendition.url, rendition.width) )
    return ','.join(sources)



@register.assignment_tag(takes_context=True)
def get_site_root(context):
    return context['request'].site.root_page

def has_menu_children(page):
    """does the current page have children in the menu?"""
    return page.get_children().live().in_menu().exists()

@register.inclusion_tag('janunde_styleguide/components/navbar/navbar.html', takes_context=True)
def navbar(context, parent, calling_page=None, transparent=False, semitrans=False, fixed=True, transparent_at=None):
    """renders the navbar"""
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.active = (calling_page.url.startswith(menuitem.url)
                           if calling_page else False)
    if not transparent_at and transparent:
        transparent_at = 100
    if semitrans:
        transparent = True
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        'request': context['request'], # needed by pageurl
        'transparent': 'transparent' if transparent  else '',
        'semitrans': 'semitrans' if semitrans  else '',
        'transparent_at': transparent_at,
        'fixed': 'fixed' if fixed else '',
        'context': context,
    }

@register.inclusion_tag('janunde_styleguide/components/navbar/navbar_children.html', takes_context=True)
def navbar_children(context, parent):
    """used by navbar to render the menu children"""
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        'request': context['request'], # needed by pageurl
    }
