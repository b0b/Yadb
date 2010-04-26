# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic.list_detail import object_list
from yawp.blog.models import Article
from tagging.models import TaggedItem

def tags_list(request, tags, page=1):
    article_list = TaggedItem.objects.get_by_model(Article, tags)

    return object_list(
        request,
        queryset = article_list,
        paginate_by = settings.ARTICLE_PER_PAGE,
        page = page,
        extra_context = {
            'tags': tags,
            'base_url': '/blog/%s' % tags,
            'message': 'Articles traitant de %s' % tags
        },
        template_object_name = 'article'
    )
