import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['nickname', 'gender', 'email',
                  'types', 'content', 'notice']

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname'].strip()
        if nickname:
            if not re.fullmatch(r'[\w.@_-]+', nickname):
                raise ValidationError('昵称包含不可识别字符', code='invalid')
        return nickname

    def clean_content(self):
        return self.cleaned_data['content'].strip()
