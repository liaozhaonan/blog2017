import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Comment, SubComment


class CommentForm(forms.ModelForm):
    "评论表单"
    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'content']

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname'].strip()
        if nickname:
            if not re.fullmatch(r'[\w.@_-]+', nickname):
                raise ValidationError('昵称包含不可识别字符', code='invalid')
        return nickname

    def clean_content(self):
        return self.cleaned_data['content'].strip()


class SubCommentForm(CommentForm):
    "评论回复表单"
    class Meta:
        model = SubComment
        fields = ['nickname', 'email', 'content']
