from janunde_styleguide.templatetags.janun_styles import register

@register.block_tag('components/header/templates/header.html')
def header(content, video=False, scroll_down_id=False, scroll_down_medium_up=False):
    """templatetag for a header

    Args:
        content (str): Content/HTML inside this header
        video (Optional[bool]): show the design video?
        scroll_down_id (Optional[str]): if present creates a button
                                        that scrolls down to #{{scroll_down_id}}
        scroll_down_medium_up (Optional[bool]): Show the scroll down button on medium up displays? default: no
    """
    if scroll_down_medium_up:
        scroll_down_extra_class = ''
    else:
        scroll_down_extra_class = 'hide-for-medium-up'
    return {
        'content': content,
        'video': video,
        'scroll_down_id': scroll_down_id,
        'scroll_down_extra_class': scroll_down_extra_class,
    }
