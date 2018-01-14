from django.contrib import admin

from .models import Message, MessageReply

# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'gender', 'email', 'types', 'content',
                    'notice', 'created_time',)


class MessageReplyAdmin(admin.ModelAdmin):
    list_display = ('related_message', 'content', 'created_time')


admin.site.register(Message, MessageAdmin)
admin.site.register(MessageReply, MessageReplyAdmin)
