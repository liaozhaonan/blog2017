from django.db import models

# Create your models here.


class Column(models.Model):
    "专栏模型"
    name = models.CharField(max_length=16, verbose_name="名字")

    class Meta:
        verbose_name_plural = verbose_name = "专栏"
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    "标签模型"
    name = models.CharField(max_length=16, verbose_name="名字")

    class Meta:
        verbose_name_plural = verbose_name = "标签"
        ordering = ['name']

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse("blog:tag", kwargs={'tag_id': self.pk})

    def __str__(self):
        return self.name


class Article(models.Model):
    "文章模型"
    title = models.CharField(max_length=128, verbose_name="标题")
    slug = models.SlugField(verbose_name="路径")
    column = models.ForeignKey("Column", verbose_name="专栏")
    tag = models.ForeignKey("Tag", verbose_name="标签")
    summary = models.TextField(verbose_name="摘要")
    content = models.TextField(verbose_name="正文")
    recommend = models.BooleanField(default=False)
    recommend_pic = models.ImageField(
        upload_to="recommend", default="recommend/default.jpg"
    )
    created_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    visited_times = models.IntegerField(default=0, verbose_name="访问次数")

    class Meta:
        verbose_name_plural = verbose_name = "文章"
        ordering = ['-created_time']

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse("blog:article", kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
