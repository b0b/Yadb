# -*- encoding: utf-8 -*-

from django.contrib.syndication.feeds import Feed
from yawp.blog.models import Article
from tagging.models import TaggedItem
from django.utils.feedgenerator import Atom1Feed
from django.contrib.comments.models import Comment

class RssArticleFeed(Feed):



    def get_object(self, keys):
        self.title = "Yawp"
        self.link = "http://www.yawp.fr/blog/"
        self.author = "Leroux Alexandre"
        self.author_link = u'http://www.yawp.fr/'
        self.feed_copyright = u'Contenu placé sous <a href="http://creativecommons.org/licenses/by/2.0/">CC-BY</a>'
        self.item_author_link = 'httpaaaa://www.example.com/' # Hard-coded author URL.

        if keys:
            key_list = keys[0].split(',')
            rub = key_list[0]
            if rub == 'comments':
                self.items = Comment.objects.filter(is_public=True, is_removed=False).order_by('-submit_date')[:15]
                self.title = u'Derniers commentaires'
                self.description = 'Liste des derniers commentaires postés'
            elif key_list:
                self.items = TaggedItem.objects.get_by_model(Article, key_list)[:15]
                self.title = u'Flux RSS pour %s' % (', '.join([tag for tag in key_list]))
                self.description = 'Derniers billets'

            else:
                raise ObjectDoesNotExist
        else:
            self.items = Article.published.order_by('-date')[:15]
            self.description = "Derniers billets parus sur Yawp"

    def item_author_link(self, obj):
        return self.author_link

class AtomArticleFeed(RssArticleFeed):
    feed_type = Atom1Feed
    #subtitle = RssArticleFeed.description
