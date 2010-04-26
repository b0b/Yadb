# -*- coding: UTF-8 -*-

from django.db import models
from datetime import datetime
from django.template.defaultfilters import slugify
from tagging.models import Tag
from tagging.fields import TagField


#class Tag(models.Model):
    #name = models.CharField('Nom', max_length=50)
    #slug = models.SlugField('Référence')

    #def get_absolute_url(self):
        #return "/blog/%s/" % (self.slug)

    #def __unicode__(self):
        #return self.name

    #def save(self):
        #self.slug = slugify(self.name)
        #super(Tag, self).save()

class ArticleManager(models.Manager):
    def get_query_set(self):
        qs = super(ArticleManager, self).get_query_set()
        return qs.filter(is_online=True, date__lte=datetime.now()).order_by('-date')

class Article(models.Model):
    title = models.CharField('Titre', max_length=100)
    slug = models.SlugField(
        'Référence',
        unique_for_date = 'date',
        max_length=60,
        #@TODO : doc : prepopulate
    )
    content = models.TextField('Contenu')
    #tags = models.ManyToManyField(Tag)
    tags = TagField()
    date = models.DateTimeField('Date de publication')

    related_article = models.ManyToManyField('self', verbose_name='Articles sur le même sujet', blank=True)
    is_online = models.BooleanField('En ligne', default=False)

    def __unicode__(self):
        return self.title

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def get_slug_tags(self):
        tags = self.get_tags()
        return ','.join([tag.name for tag in tags])

    def get_absolute_url(self):
        return '/blog/%s/%s/' % (self.get_slug_tags(), self.slug)

    def save(self):
        if not self.id:
            self.date = datetime.now()

        self.slug = slugify(self.title)
        super(Article, self).save()

    published = ArticleManager()
