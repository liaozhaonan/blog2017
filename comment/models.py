from django.db import models

from blog.models import Article

# Create your models here.


class Comment(models.Model):
    "评论模型"
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    email = models.EmailField(verbose_name='邮箱')
    content = models.TextField(max_length=1000, verbose_name='内容')
    up_times = models.IntegerField(default=0, verbose_name='赞同')
    related_article = models.ForeignKey(Article, verbose_name='文章')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = "评论"
        ordering = ['created_time']

    def __str__(self):
        return self.nickname + '的评论'


class SubComment(models.Model):
    "评论回复模型"
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    email = models.EmailField(verbose_name='邮箱')
    content = models.TextField(max_length=1000, verbose_name='内容')
    related_comment = models.ForeignKey(Comment, verbose_name='评论')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = "评论回复"
        ordering = ['created_time']

    def __str__(self):
        return self.nickname + '的评论回复'
