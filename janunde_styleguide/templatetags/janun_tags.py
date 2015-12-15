from django import template
register = template.Library()


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    return context['request'].site.root_page

def has_menu_children(page):
    """does the current page have children in the menu?"""
    return page.get_children().live().in_menu().exists()

@register.inclusion_tag('janunde_styleguide/components/navbar/navbar.html', takes_context=True)
def navbar(context, parent, calling_page=None, transparent=False, fixed=True):
    """renders the navbar"""
    menuitems = parent.get_children().live().in_menu()
    print(parent)
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.active = (calling_page.url.startswith(menuitem.url)
                           if calling_page else False)
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        'request': context['request'], # needed by pageurl
        'transparent': 'transparent' if transparent  else '',
        'fixed': 'fixed' if fixed else '',
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
