from janunde_styleguide.templatetags.janun_styles import register

@register.inclusion_tag('patterns/colors/templates/colorbox.html')
def colorbox(color):
    return {'color': color}
