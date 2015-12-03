from janunde_styleguide.templatetags.janun_styles import register

@register.block_tag('components/teaser/templates/teaser.html')
def teaser(content):
    """templatetag for a teaser
    """
    return {
        'content': content,
    }
