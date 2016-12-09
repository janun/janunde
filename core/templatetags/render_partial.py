from django.template import Context
from django import template
register = template.Library()


@register.tag
def render_partial(parser, token):
    tagname, object = token.split_contents()
    return PartialNode(object)

class PartialNode(template.Node):
    def __init__(self, object):
        self.object = template.Variable(object)

    def render(self, context):
        try:
            object = self.object.resolve(context).specific
        except template.VariableDoesNotExist:
            return ''
        template_name = object.partial_template_name
        t = context.template.engine.get_template(template_name)
        context['object'] = object
        return t.render(context)
