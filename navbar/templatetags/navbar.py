from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def submenu_active(context, submenu, current_page):
    """If any of the submenu items are active"""
    for category in submenu:
        for item in category.value["submenu"]:
            if item.value["page"].url == current_page.url:
                return True
    return False


@register.filter()
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False
