from django.test import TestCase
from django.core.urlresolvers import reverse

from blog.models import Article, Column, Tag
from .models import Comment
from .forms import CommentForm, SubCommentForm

# Create your tests here.


class CommentFormTest(TestCase):
    "测试评论表单"

    def setUp(self):
        self.comment = {
            'nickname': 'testClient',
            'email': 'test@example.com',
            'content': 'my comment for test'
        }

    def test_attrs_cannot_empty(self):
        f = CommentForm({})
        self.assertFalse(f.is_valid())
        self.assertTrue(f['nickname'].errors)
        self.assertTrue(f['email'].errors)
        self.assertTrue(f['content'].errors)

    def test_nickname_restrict_character(self):
        f = CommentForm(self.comment)
        self.assertTrue(f.is_valid())
        self.comment['nickname'] = '我的test'
        f = CommentForm(self.comment)
        self.assertTrue(f.is_valid())
        self.comment['nickname'] = '$'
        f = CommentForm(self.comment)
        self.assertFalse(f.is_valid())
        self.comment['nickname'] = '空格 space'
        f = CommentForm(self.comment)
        self.assertFalse(f.is_valid())

    def test_email_pattern(self):
        self.comment['email'] = 'test'
        f = CommentForm(self.comment)
        self.assertFalse(f.is_valid())
        self.comment['email'] = 'test@example'
        f = CommentForm(self.comment)
        self.assertFalse(f.is_valid())
        self.comment['email'] = 'test@example.'
        f = CommentForm(self.comment)
        self.assertFalse(f.is_valid())
        self.comment['email'] = 'test@example.com.cn'
        f = CommentForm(self.comment)
        self.assertTrue(f.is_valid())

    def test_content_limit_1000(self):
        self.comment['content'] = '表单测试' * 250
        f = CommentForm(self.comment)
        self.assertTrue(f.is_valid())
        self.comment['content'] = '表单测试' * 251
        f = CommentForm(self.comment)
        self.assertFalse(f.is_valid())


class SubCommentFormTest(TestCase):
    "测试回复表单"

    def setUp(self):
        self.subcomment = {
            'nickname': 'testClient',
            'email': 'test@example.com',
            'content': 'my subcomment for test'
        }

    def test_attrs_cannot_empty(self):
        f = SubCommentForm({})
        self.assertFalse(f.is_valid())
        self.assertTrue(f['nickname'].errors)
        self.assertTrue(f['email'].errors)
        self.assertTrue(f['content'].errors)

    def test_nickname_restrict_character(self):
        f = SubCommentForm(self.subcomment)
        self.assertTrue(f.is_valid())
        self.subcomment['nickname'] = '我的test'
        f = SubCommentForm(self.subcomment)
        self.assertTrue(f.is_valid())
        self.subcomment['nickname'] = '$'
        f = SubCommentForm(self.subcomment)
        self.assertFalse(f.is_valid())
        self.subcomment['nickname'] = '空格 space'
        f = SubCommentForm(self.subcomment)
        self.assertFalse(f.is_valid())

    def test_email_pattern(self):
        self.subcomment['email'] = 'test'
        f = SubCommentForm(self.subcomment)
        self.assertFalse(f.is_valid())
        self.subcomment['email'] = 'test@example'
        f = SubCommentForm(self.subcomment)
        self.assertFalse(f.is_valid())
        self.subcomment['email'] = 'test@example.'
        f = SubCommentForm(self.subcomment)
        self.assertFalse(f.is_valid())
        self.subcomment['email'] = 'test@example.com.cn'
        f = SubCommentForm(self.subcomment)
        self.assertTrue(f.is_valid())

    def test_content_limit_1000(self):
        self.subcomment['content'] = '表单测试' * 250
        f = SubCommentForm(self.subcomment)
        self.assertTrue(f.is_valid())
        self.subcomment['content'] = '表单测试' * 251
        f = SubCommentForm(self.subcomment)
        self.assertFalse(f.is_valid())


class CommentCreateViewTests(TestCase):
    "测试评论创建视图"

    def setUp(self):
        column = Column.objects.create(name='comment_test')
        tag = Tag.objects.create(name='comment_test')
        self.article = Article.objects.create(
            title='comment test',
            slug='comment-test',
            column=column,
            tag=tag,
            summary='my article summary',
            content='my article content'
        )
        self.comment = {
            'nickname': 'testClient',
            'email': 'test@example.com',
            'content': 'my comment for test'
        }

    def test_form_valid(self):
        response = self.client.post(
            reverse('comment:comment-create',
                    kwargs={'slug': self.article.slug}),
            self.comment
        )
        self.assertTrue(response.status_code, 302)

    def test_form_invalid(self):
        self.comment['nickname'] = ''
        response = self.client.post(
            reverse('comment:comment-create',
                    kwargs={'slug': self.article.slug}),
            self.comment
        )
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '评论失败')


class CommentUpvoteTests(TestCase):
    "测试评论点赞视图"

    def setUp(self):
        column = Column.objects.create(name='subcomment_test')
        tag = Tag.objects.create(name='subcomment_test')
        article = Article.objects.create(
            title='subcomment test',
            slug='subcomment-test',
            column=column,
            tag=tag,
            summary='my article summary',
            content='my article content'
        )
        self.comment = Comment.objects.create(
            nickname='testClient',
            email='test@example.com',
            content='my comment content',
            related_article=article
        )

        def test_upvote(self):  # 点赞
            response = self.client.post(
                reverse('comment:comment-upvote',
                        kwargs={'comment_id': self.comment.id}),
                {'addNum': 1}
            )
            self.assertTrue(response.status_code, 200)
            self.assertContains(response, '1')

        def test_revoke_upvote(self):  # 取消点赞
            response = self.client.post(
                reverse('comment:comment-upvote',
                        kwargs={'comment_id': self.comment.id}),
                {'addNum': -1}
            )
            self.assertTrue(response.status_code, 200)
            self.assertContains(response, '-1')

        def test_upvote_invalid(self):
            response = self.client.post(
                reverse('comment:comment-upvote',
                        kwargs={'comment_id': self.comment.id}),
                {'addNum': None}
            )
            self.assertTrue(response.status_code, 403)
            response = self.client.post(
                reverse('comment:comment-upvote',
                        kwargs={'comment_id': self.comment.id}),
                {'addNum': 2}
            )
            self.assertTrue(response.status_code, 403)
            response = self.client.post(
                reverse('comment:comment-upvote',
                        kwargs={'comment_id': self.comment.id}),
                {'addNum': -2}
            )
            self.assertTrue(response.status_code, 403)


class SubCommentCreateViewTests(TestCase):
    "测试回复评论视图"

    def setUp(self):
        column = Column.objects.create(name='subcomment_test')
        tag = Tag.objects.create(name='subcomment_test')
        article = Article.objects.create(
            title='subcomment test',
            slug='subcomment-test',
            column=column,
            tag=tag,
            summary='my article summary',
            content='my article content'
        )
        self.comment = Comment.objects.create(
            nickname='testClient',
            email='test@example.com',
            content='my comment content',
            related_article=article
        )
        self.subcomment = {
            'nickname': 'testClient',
            'email': 'test@example.com',
            'content': 'my subcomment content'
        }

    def test_form_valid(self):
        response = self.client.post(
            reverse('comment:subcomment-create',
                    kwargs={'comment_id': self.comment.id}),
            self.subcomment
        )
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '回复成功')

    def test_form_invalid(self):
        self.subcomment['nickname'] = ''
        response = self.client.post(
            reverse('comment:subcomment-create',
                    kwargs={'comment_id': self.comment.id}),
            self.subcomment
        )
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '回复失败')
