from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Column, Tag, Article
# Create your tests here.


class TagModelMethodTests(TestCase):
    "测试标签模型的方法"

    def setUp(self):
        self.tag = Tag.objects.create(name='myTag1')

    def test_tag_get_absolute_url(self):
        from django.core.urlresolvers import reverse
        self.assertEqual(self.tag.get_absolute_url(),
                         '/blog/tag/' + str(self.tag.pk) + '/')


class ArticleModelMethodTests(TestCase):
    "测试文章模型的方法"

    def setUp(self):
        column = Column.objects.create(name='myColumn2')
        tag = Tag.objects.create(name="myTag2")
        self.article = Article.objects.create(
            title='my article',
            slug='my-article',
            column=column,
            tag=tag,
            summary='my article summary',
            content='my article content'
        )

    def test_article_get_absolute_url(self):
        self.assertEqual(self.article.get_absolute_url(),
                         '/blog/article/' + str(self.article.slug))


class HomeViewTests(TestCase):
    "测试首页视图"

    def test_home_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class BlogViewTests(TestCase):
    "测试博客页视图"

    def test_blog_status_code(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)


class ArticleViewTests(TestCase):
    "测试文章页视图"

    def setUp(self):
        column = Column.objects.create(name='myColumn3')
        tag = Tag.objects.create(name="myTag3")
        self.article = Article.objects.create(
            title='my article3',
            slug='my-article3',
            column=column,
            tag=tag,
            summary='my article summary',
            content='my article content'
        )

    def test_article_status_code(self):
        response = self.client.get(
            reverse('blog:article', kwargs={'slug': self.article.slug}))
        self.assertEqual(response.status_code, 200)

    def test_article_status_code_with_not_exist_slug(self):
        response = self.client.get(
            reverse('blog:article', kwargs={'slug': 'not-exist-article'}))
        self.assertEqual(response.status_code, 404)


class ArchiveViewTest(TestCase):
    "测试归档页视图"

    def setUp(self):
        self.year = timezone.datetime.today().year

    def test_archive_with_current_year(self):
        response = self.client.get(
            reverse('blog:archive', kwargs={'year': self.year}))
        self.assertEqual(response.status_code, 200)

    def test_archive_with_passed_year(self):
        response1 = self.client.get(
            reverse('blog:archive', kwargs={'year': self.year - 5}))
        response2 = self.client.get(
            reverse('blog:archive', kwargs={'year': self.year - 10}))
        self.assertEqual(response1.status_code, 404)
        self.assertEqual(response2.status_code, 404)

    def test_archive_with_future_year(self):
        response1 = self.client.get(
            reverse('blog:archive', kwargs={'year': self.year + 10}))
        response2 = self.client.get(
            reverse('blog:archive', kwargs={'year': self.year + 50}))
        self.assertEqual(response1.status_code, 404)
        self.assertEqual(response2.status_code, 404)


class TagViewTests(TestCase):
    "测试标签页视图"

    def setUp(self):
        self.tag = Tag.objects.create(name="myTag3")

    def test_tag_status_code(self):
        response = self.client.get(
            reverse('blog:tag', kwargs={'tag_id': self.tag.id}))
        self.assertEqual(response.status_code, 200)

    def test_tag_status_code_with_not_exist_id(self):
        response = self.client.get(
            reverse('blog:tag', kwargs={'tag_id': 99}))
        self.assertEqual(response.status_code, 404)


class SearchViewTests(TestCase):
    "测试搜索视图"

    def test_search_with_good_keyword(self):
        response1 = self.client.get(reverse('blog:search') + "?key=test's")
        response2 = self.client.get(reverse('blog:search') + "?key=测试")
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response1, '结果')
        self.assertContains(response2, '结果')

    def test_search_with_bad_keyword(self):
        response1 = self.client.get(reverse('blog:search') + '?key=')
        response2 = self.client.get(reverse('blog:search') + '?key=#*')
        response3 = self.client.get(reverse('blog:search') + '?key=@#$#%')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)
        self.assertContains(response1, '请输入有效搜索关键词')
        self.assertContains(response2, '请输入有效搜索关键词')
        self.assertContains(response3, '请输入有效搜索关键词')
