# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.views.generic.list_detail import object_list, object_detail
from yawp.blog.models import Article
from yawp.blog.views import tags_list

page_re = '(?P<page>[0-9]+)'
slug_re = '(?P<slug>[-\w]+)'
tags = '([-\w]+,)*[-\w]+'
tags_re = '(?P<tags>%s)' % tags

article_dict = dict(
    queryset = Article.published.all(),
    template_object_name = 'article',
    paginate_by = settings.ARTICLE_PER_PAGE,
    extra_context = {
        'base_url': '/blog',
        'message': 'Derniers billets',
    },
)

urlpatterns = patterns('yawp.blog.views',
    # Liste des articles
    url(r'^$', object_list, article_dict, name='blog'),
    url(r'^page/%(page_re)s/$' % locals(), object_list, article_dict),

    # Article
    url(r'^%(tags)s/%(slug_re)s/$' % locals(),
        object_detail,
        dict(
            queryset = Article.published.all(),
            template_object_name = 'article',
            slug_field = 'slug',
        ),
    ),

    # Tags
    url(r'^%(tags_re)s/$' % locals(), tags_list),
    url(r'^%(tags_re)s/page/%(page_re)s/$' % locals(), tags_list)
)
