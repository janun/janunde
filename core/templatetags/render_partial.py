from django import template

register = template.Library()


@register.tag
def render_partial(parser, token):
    _, obj = token.split_contents()
    return PartialNode(obj)


class PartialNode(template.Node):
    def __init__(self, obj):
        self.object = template.Variable(obj)

    def render(self, context):
        try:
            obj = self.object.resolve(context).specific
        except template.VariableDoesNotExist:
            return ""
        template_name = obj.partial_template_name
        t = context.template.engine.get_template(template_name)
        context["object"] = obj
        return t.render(context)
