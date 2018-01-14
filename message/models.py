from django.db import models
from django.core.mail import send_mail
# Create your models here.


class Message(models.Model):
    "留言模型"
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )
    TYPES_CHOICES = (
        ('P', '编程'),
        ('O', '其他'),
    )
    nickname = models.CharField(max_length=32, verbose_name="昵称")
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES,
                              default="M", verbose_name="性别")
    email = models.EmailField(verbose_name="邮箱")
    types = models.CharField(max_length=2, choices=TYPES_CHOICES,
                             default="O", verbose_name="分类")
    content = models.TextField(max_length=500, verbose_name="内容")
    notice = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = "留言"
        ordering = ['-created_time']

    def __str__(self):
        return self.nickname + '的留言'


class MessageReply(models.Model):
    "留言回复模型"
    related_message = models.OneToOneField(Message, verbose_name="留言")
    content = models.TextField(max_length=500, verbose_name="回复", default=None)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = "留言回复"
        ordering = ['-created_time']

    def save(self):
        super(MessageReply, self).save()
        # 发送回复提醒邮件
        if self.related_message.notice:
            string = '''亲爱的网友，你好！你在 www.xxx.com 上的留言:\n
                %s \n\n有回复啦！回复内容如下：\n
                %s\n\n<如果你没有在本网站上提交过留言，请忽略本邮件。>
                ''' % (self.related_message.content, self.content)
            send_mail('留言回复提醒', string, 'Jonah博客 <lzn_189boy@163.com>',
                      ['%s' % self.related_message.email], fail_silently=False)

    def __str__(self):
        return '回复' + self.related_message.nickname + '的留言'
