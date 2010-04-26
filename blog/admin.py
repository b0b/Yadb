from yawp.blog.models import Article
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Infos',   {'fields': ['title', 'date', 'tags', 'related_article', 'is_online']}),
        ('Message', {'fields': ['content']}), #, 'classes': ['collapse']}),
    ]

    list_display = ('title', 'date', 'is_online' )
    list_filter = ['date']
    search_fields = ['title', 'content']
    date_hierarchy = 'date'

admin.site.register(Article, ArticleAdmin)
