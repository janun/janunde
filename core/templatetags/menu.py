from collections import defaultdict

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    try:
        return context["request"].site.root_page
    except KeyError:
        return None


def get_children(page):
    return page.get_children().live().in_menu().specific()


# def group_by_category(pages) -> dict:
#     """Group menu items by their megamenu_category

#     Example:
#         group_by_category([page1, page2, page3]) returns:
#         {
#             "": [page1],
#             "category": [page2, page3]
#         }
#     """
#     result = defaultdict(list)
#     for page in pages:
#         result[page.megamenu_category or ""].append(page)
#     return result


def is_active(page, calling_page, exact=False) -> bool:
    """wether a given page is active"""
    try:
        if exact:
            return calling_page.url == page.url
        return calling_page.url.startswith(page.url)
    except AttributeError:
        return False


@register.simple_tag(takes_context=True)
def get_menuitems(context, parent, calling_page=None):
    """gets menuitems"""
    menuitems = get_children(parent)

    for menuitem in menuitems:
        menuitem.children = list(get_children(menuitem))

        if menuitem.children:
            for child in menuitem.children:
                child.is_active = is_active(child, calling_page)
                if child.is_active:
                    menuitem.active_child = True

            menuitem.children += [menuitem]
            menuitem.children = sorted(
                menuitem.children, key=lambda p: (p.megamenu_category or "", p.title)
            )
            menuitem.is_active = is_active(menuitem, calling_page, exact=True)
        else:
            menuitem.is_active = is_active(menuitem, calling_page)
    return menuitems
