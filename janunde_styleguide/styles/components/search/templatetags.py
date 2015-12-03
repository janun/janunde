from janunde_styleguide.templatetags.janun_styles import register

@register.inclusion_tag('components/search/templates/search.html')
def search(css_classes=None, animate=False):
    if not css_classes:
        css_classes = []
    if animate:
        css_classes.append('animate')
        css_classes.append('closed')
    return {
        'css_classes': ' '.join(css_classes),
    }
