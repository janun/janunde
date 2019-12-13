import os

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from wagtail.core.models import Page
from wagtail.search.models import Query

from django.http import HttpResponse
from django.http import Http404

from django.shortcuts import get_object_or_404


from core.models import JanunTag
Tag = JanunTag.tag_model()

def tags(request, tagname):
    tag = get_object_or_404(Tag, name__iexact=tagname)

    if tag.thema.all():
        thema = tag.thema.all()[0]
        tagname = thema.title
    else:
        thema = None

    objects = []
    for relation in JanunTag.objects.filter(tag=tag.id):
        objects.append(relation.content_object.specific)

    return render(request, 'core/thema.html', {
            'tagname': tagname,
            'objects': objects,
            'thema': thema,
        })
