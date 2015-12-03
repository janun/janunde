from django.template.base import Library, TagHelperNode, Template, parse_bits
from inspect import getargspec, getcallargs
from functools import partial
from django.utils import six


def generic_tag_compiler(parser, token, params, varargs, varkw, defaults,
                         name, takes_context, node_class):
    bits = token.split_contents()[1:]
    if 'content' in params:
        params.remove('content')
    args, kwargs = parse_bits(parser, bits, params, varargs, varkw,
                              defaults, takes_context, name)
    nodelist = parser.parse(('end%s' % name,))
    parser.delete_first_token()
    return node_class(takes_context, args, kwargs, nodelist)


class JanunTagLibrary(Library):

    def block_tag(self, file_name, takes_context=False, name=None):
        def dec(func):
            params, varargs, varkw, defaults = getargspec(func)

            class BlockNode(TagHelperNode):

                def __init__(self, takes_context, args, kwargs, nodelist=None):
                    self.takes_context = takes_context
                    self.args = args
                    self.kwargs = kwargs
                    self.nodelist = nodelist

                def render(self, context):
                    """
                    Renders the specified template and context. Caches the
                    template object in render_context to avoid reparsing and
                    loading when used in a for loop.
                    """
                    resolved_args, resolved_kwargs = self.get_resolved_arguments(context)
                    resolved_args.insert(0, self.nodelist.render({}))
                    _dict = func(*resolved_args, **resolved_kwargs)

                    t = context.render_context.get(self)
                    if t is None:
                        if isinstance(file_name, Template):
                            t = file_name
                        elif isinstance(getattr(file_name, 'template', None), Template):
                            t = file_name.template
                        elif not isinstance(file_name, six.string_types) and is_iterable(file_name):
                            t = context.template.engine.select_template(file_name)
                        else:
                            t = context.template.engine.get_template(file_name)
                        context.render_context[self] = t
                    new_context = context.new(_dict)
                    # Copy across the CSRF token, if present, because
                    # inclusion tags are often used for forms, and we need
                    # instructions for using CSRF protection to be as simple
                    # as possible.
                    csrf_token = context.get('csrf_token', None)
                    if csrf_token is not None:
                        new_context['csrf_token'] = csrf_token
                    return t.render(new_context)

            function_name = (name or
                getattr(func, '_decorated_function', func).__name__)
            compile_func = partial(generic_tag_compiler,
                params=params, varargs=varargs, varkw=varkw,
                defaults=defaults, name=function_name,
                takes_context=takes_context, node_class=BlockNode)
            compile_func.__doc__ = func.__doc__
            self.tag(function_name, compile_func)
            return func
        return dec
