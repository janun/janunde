from django import template
register = template.Library()


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    try:
        return context['request'].site.root_page
    except KeyError:
        return None


def get_children(page):
    return page.get_children().live().in_menu()


@register.assignment_tag(takes_context=True)
def get_menuitems(context, parent, calling_page=None):
    """gets menuitems"""
    menuitems = get_children(parent)

    for menuitem in menuitems:
        menuitem.children = get_children(menuitem)
        menuitem.is_active = (calling_page.url.startswith(menuitem.url)
                               if calling_page else False)
    return menuitems
