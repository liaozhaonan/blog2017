from django.contrib import admin

from .models import Comment, SubComment

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'email', 'related_article', 'content',
                    'created_time', 'up_times')


class SubCommentAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'email', 'related_comment', 'content',
                    'created_time')


admin.site.register(Comment, CommentAdmin)
admin.site.register(SubComment, SubCommentAdmin)
