# -*- coding: UTF-8 -*-

import re

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.generic.list_detail import object_list
from yawp.blog.models import Article
from yawp.search.forms import SearchForm


# ``normalize_query`` and ``get_query methods`` come from this blog post
# http://www.julienphalip.com/blog/2008/08/16/adding-search-django-site-snap/

def normalize_query(
        query_string,
        findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
        normspace=re.compile(r'\s{2,}').sub
    ):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    query = None
    terms = normalize_query(query_string)

    for term in terms:
        or_query = None # Query to search for a given term in each field

        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query

    return query

def search_redirect(request):
    if 'search_terms' in request.REQUEST:
        form = SearchForm(request.REQUEST)
        if form.is_valid():
            search_terms = [term for term in form.cleaned_data['search_terms'].split()]
            return HttpResponseRedirect('/recherche/%s/' % ','.join(search_terms))

    return HttpResponseRedirect('/')

def search(request):
    query_string = ''
    found_entries = None

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        post_query = get_query(query_string, ['title', 'content'])
        post_queryset = Article.published.filter(post_query)

        terms_list = normalize_query(query_string)
        terms = ' '.join([term for term in terms_list])

        return object_list(
            request,
            queryset = post_queryset,
            paginate_by = settings.ARTICLE_PER_PAGE,
            extra_context = {
                'message': 'Articles parlant de \"%s\"' % terms,
            },
            template_object_name = 'article'
        )
    else:
        return HttpResponseRedirect('/blog/')
