from janunde_styleguide.templatetags.janun_styles import register

@register.block_tag('components/panels/templates/panel.html')
def panel(content, heading="", picture="", ellipsize=False, css_class=''):
    return {
        'content': content,
        'heading': heading,
        'picture': picture,
        'ellipsize': 'ellipsize' if ellipsize else '',
        'css_class': css_class,
    }
