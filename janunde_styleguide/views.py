from django.shortcuts import render
from django.http import Http404
from django.template import TemplateDoesNotExist
from .utils import get_pages


def index(request):
    return render(request, "janunde_styleguide/index.html", {'pages': get_pages()})

def page(request, path):
    try:
        return render(request, "%s/_doc.html" % path, {'pages': get_pages()})
    except TemplateDoesNotExist:
        raise Http404
