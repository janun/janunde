from janunde_styleguide.templatetags.janun_styles import register

@register.inclusion_tag('components/navbar/templates/navbar.html')
def navbar(css_classes=None, fixed=False, transparent=False):
    if not css_classes:
        css_classes = []
    if fixed:
        css_classes.append('fixed')
    if transparent:
        css_classes.append('transparent')
    return {
        'css_classes': ' '.join(css_classes),
    }
