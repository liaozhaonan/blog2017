from django.test import TestCase
from django.core.urlresolvers import reverse

from .forms import MessageForm

# Create your tests here.


class MessageFormTest(TestCase):
    "测试留言表单"

    def setUp(self):
        self.message = {
            'nickname': 'testClient',
            'email': 'test@example.com',
            'content': 'my message for test',
            'gender': 'M',
            'types': 'O'
        }

    def test_attrs_cannot_empty(self):
        f = MessageForm({})
        self.assertFalse(f.is_valid())
        self.assertTrue(f['nickname'].errors)
        self.assertTrue(f['email'].errors)
        self.assertTrue(f['content'].errors)

    def test_nickname_restrict_character(self):
        f = MessageForm(self.message)
        self.assertTrue(f.is_valid())
        self.message['nickname'] = '我的test'
        f = MessageForm(self.message)
        self.assertTrue(f.is_valid())
        self.message['nickname'] = '$'
        f = MessageForm(self.message)
        self.assertFalse(f.is_valid())
        self.message['nickname'] = '空格 space'
        f = MessageForm(self.message)
        self.assertFalse(f.is_valid())

    def test_email_pattern(self):
        self.message['email'] = 'test'
        f = MessageForm(self.message)
        self.assertFalse(f.is_valid())
        self.message['email'] = 'test@example'
        f = MessageForm(self.message)
        self.assertFalse(f.is_valid())
        self.message['email'] = 'test@example.'
        f = MessageForm(self.message)
        self.assertFalse(f.is_valid())
        self.message['email'] = 'test@example.com.cn'
        f = MessageForm(self.message)
        self.assertTrue(f.is_valid())

    def test_content_limit_500(self):
        self.message['content'] = '表单测试' * 125
        f = MessageForm(self.message)
        self.assertTrue(f.is_valid())
        self.message['content'] = '表单测试' * 126
        f = MessageForm(self.message)
        self.assertFalse(f.is_valid())


class MessageViewTests(TestCase):
    "测试留言页面视图"

    def test_valid_types(self):
        response = self.client.get(reverse('message:index'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('message:index') + '?types=')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('message:index') + '?types=all')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('message:index') + '?types=programming'
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('message:index') + '?types=others')
        self.assertEqual(response.status_code, 200)

    def test_invalid_types(self):
        response = self.client.get(reverse('message:index') + '?types=invalid')
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('message:index') + '?types=无效')
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('message:index') + '?types=1')
        self.assertEqual(response.status_code, 404)


class MessageCreateViewTests(TestCase):
    "测试留言创建视图"

    def setUp(self):
        self.message = {
            'nickname': 'testClient',
            'gender': 'F',
            'email': 'test@example.com',
            'types': 'P',
            'content': 'my message2 for test'

        }

    def test_form_valid(self):
        response = self.client.post(reverse('message:create'), self.message)
        self.assertTrue(response.status_code, 302)

    def test_form_invalid(self):
        self.message['nickname'] = ''
        response = self.client.post(reverse('message:create'), self.message)
        self.assertTrue(response.status_code, 302)
        self.assertContains(response, '留言失败')


class AjaxSuccessTests(TestCase):
    "测试异步留言成功视图"

    def test_ajax_success(self):
        response = self.client.post(reverse('message:ajax-success'))
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '留言成功')
