import re

from django.shortcuts import get_object_or_404, Http404, HttpResponse
from django.core.cache import caches
from django.views.generic.list import ListView
from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from comment.models import Comment
from .models import Article, Column, Tag

# Create your views here.
# 缓存
try:
    CACHE = caches['memcache']
except ImportError:
    CACHE = caches['default']


class ArticleMixin(object):
    articles = Article.objects.all()


class ColumnMixin(object):
    columns = Column.objects.all()


class TagMixin(object):
    tags = Tag.objects.all()


class HomeView(ArticleMixin, ListView):
    "首页视图"
    template_name = 'home.html'

    def get_queryset(self):
        return self.articles

    def get_context_data(self, **kwargs):
        kwargs['recents'] = self.articles[:7]  # 最近文章
        kwargs['hots'] = self.articles.order_by('-visited_times')[:7]  # 热门文章
        kwargs['recommends'] = self.articles.filter(recommend=True)  # 推荐文章
        kwargs['notice'] = settings.NOTICE  # 通知框内容
        return super(HomeView, self).get_context_data(**kwargs)


class BlogView(ArticleMixin, ColumnMixin, TagMixin, ListView):
    "博客页视图"
    context_object_name = 'articles'
    paginate_by = settings.PAGE_NUM  # 分页

    def get_template_names(self):
        if self.request.is_ajax():
            return 'widgets/article-list.html'  # ajax请求时使用的模板
        return 'blog.html'

    def get_queryset(self):
        column_id = self.request.GET.get('column_id', '')

        # 如果请求包含关键字参数column_id,返回对应专栏的文章,否则返回所有文章作为queryset
        if column_id:
            self.column = get_object_or_404(self.columns, id=column_id)
            articles = self.articles.filter(column=self.column.id)
        else:
            self.column = None
            articles = self.articles

        return articles

    def get_archives(self):
        "按年份归档并返回每年的文章数目"
        archives = dict()
        current_year = timezone.datetime.today().year

        for year in range(2017, current_year + 1):
            num = len(self.articles.filter(created_time__year=year))
            archives[year] = num

        return archives

    def get_context_data(self, **kwargs):
        kwargs['tags'] = self.tags  # 标签
        kwargs['tags_num'] = len(self.tags)  # 标签数目
        kwargs['columns'] = self.columns  # 所有专栏
        kwargs['this_column'] = self.column  # 请求的专栏
        kwargs['archives'] = self.get_archives()  # 归档
        return super(BlogView, self).get_context_data(**kwargs)


class ArticleView(ArticleMixin, ListView):
    "详细呈现一篇文章, 分页获取文章评论"
    context_object_name = 'comments'
    paginate_by = settings.PAGE_NUM

    def get_template_names(self):
        if self.request.is_ajax():
            return 'widgets/comment-list.html'
        return 'article-detail.html'

    def get_queryset(self):
        return Comment.objects.filter(related_article=self.article)  # 获取评论

    def get_context_data(self, **kwargs):
        page = self.request.GET.get('page', '')
        try:
            # 前面的评论数目
            # 如获取第 3 页评论(page=3),每页先是10条评论,则 prev_mun = (3-1)*10 = 20
            # 从而可知, 第 3 页获取的是第 21 条到第 30 条评论(共10条)
            prev_num = (int(page) - 1) * settings.PAGE_NUM
        except ValueError:
            # 请求没有提交page参数时, 返回第 1 页评论, prev_num = 0
            prev_num = 0
        kwargs['prev_num'] = prev_num
        kwargs['article'] = self.article
        return super(ArticleView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        self.article = get_object_or_404(self.articles, slug=slug)

        # 统计文章被访问次数
        if 'HTTP_X_FORWARDED_FOR' in self.request.META:
            current_ip = self.request.META['HTTP_X_FORWARDED_FOR']
        else:
            current_ip = self.request.META['REMOTE_ADDR']

        # 获取15*60s时间内访问过这篇文章的所有ip
        visited_ips = CACHE.get(slug, [])

        # 如果ip不存在则浏览次数+1
        if current_ip not in visited_ips:
            self.article.visited_times += 1
            self.article.save()
            visited_ips.append(current_ip)

            # 更新缓存
            CACHE.set(slug, visited_ips, 15 * 60)

        return super(ArticleView, self).get(request, *args, **kwargs)


class SearchView(ArticleMixin, ListView):
    "按搜索的关键词,返回文章的搜索结果"
    context_object_name = 'articles'
    paginate_by = settings.PAGE_NUM

    def get_template_names(self):
        if self.request.is_ajax():
            return 'widgets/article-list.html'
        return 'search-result.html'

    def get_queryset(self):
        # 在文章题目,概要和内容中查找并返回含有该关键词的文章
        articles = self.articles.filter(
            Q(title__icontains=self.key) | Q(summary__icontains=self.key) |
            Q(content__icontains=self.key)
        )
        self.count = len(articles)
        return articles

    def get_context_data(self, **kwargs):
        kwargs['key'] = self.key
        kwargs['count'] = self.count
        return super(SearchView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        key = self.request.GET.get('key', '').strip()  # 搜索关键词
        if key:
            reg = re.compile(r'[\w\'-]')
            self.key = ''.join([k for k in list(key) if reg.match(k)])
        else:
            self.key = ''
        if not self.key:
            return HttpResponse("<h3>请输入有效搜索关键词</h3>")
        return super(SearchView, self).get(request, *args, **kwargs)


class TagView(ArticleMixin, TagMixin, ListView):
    "标签视图, 返回该标签的对应文章的列表"
    context_object_name = 'articles'
    paginate_by = settings.PAGE_NUM

    def get_template_names(self):
        if self.request.is_ajax():
            return 'widgets/article-list.html'
        return 'tag.html'

    def get_queryset(self):
        tag_id = self.kwargs.get('tag_id')
        self.tag = get_object_or_404(self.tags, id=tag_id)
        articles = self.articles.filter(tag=self.tag.id)  # 获取该标签的文章
        self.count = len(articles)
        return articles

    def get_context_data(self, **kwargs):
        kwargs['tag'] = self.tag
        kwargs['count'] = self.count
        return super(TagView, self).get_context_data(**kwargs)


class ArchiveView(ArticleMixin, ListView):
    "归档视图, 按年份对文章进行归档, 返回某年的所有文章"
    context_object_name = 'articles'
    template_name = 'archive.html'

    def get_queryset(self):
        self.year = self.kwargs.get('year')
        current_year = timezone.datetime.today().year

        if int(self.year) not in range(2017, current_year + 1):
            raise Http404

        articles = self.articles.filter(created_time__year=self.year)
        self.count = len(articles)
        return articles

    def get_context_data(self, **kwargs):
        kwargs['year'] = self.year
        kwargs['count'] = self.count
        return super(ArchiveView, self).get_context_data(**kwargs)
