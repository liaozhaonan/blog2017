from django.contrib import admin

from .models import Column, Tag, Article

# Register your models here.


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'column', 'tag', 'summary', 'content',
                    'created_time', 'visited_times')


admin.site.register(Column, ColumnAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
