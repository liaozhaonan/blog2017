from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, render_to_response)
from django.http import HttpResponseBadRequest
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_http_methods

from blog.models import Article
from .models import Comment, SubComment
from .forms import CommentForm, SubCommentForm

# Create your views here.


class CommentCreateView(CreateView):
    "创建评论"
    form_class = CommentForm
    template_name = 'article-detail.html'

    def get_success_url(self):
        return '/article/' + self.slug  # 跳转到文章页

    def form_valid(self, form):
        self.slug = self.kwargs.get('slug')
        com = Comment()
        com.nickname = form.cleaned_data['nickname']
        com.email = form.cleaned_data['email']
        com.content = form.cleaned_data['content']
        com.related_article = get_object_or_404(Article, slug=self.slug)
        com.save()
        if self.request.is_ajax():
            return render_to_response('widgets/comment-new.html',
                                      {'comment': com})
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        self.slug = self.kwargs.get('slug')
        if self.request.is_ajax():
            return render_to_response('widgets/form-ajax-invalid.html',
                                      self.get_context_data(form=form))
        return self.render_to_response(self.get_context_data(form=form,
                                                             slug=self.slug))


@require_http_methods(['POST'])
def comment_upvote(request, comment_id):
    "点赞及取消点赞"
    comment = get_object_or_404(Comment, id=comment_id)
    num = request.POST.get('addNum', '')

    try:
        num = int(num)
    except ValueError:
        raise HttpResponseBadRequest()

    # 点赞为 1, 取消点赞为 -1
    if num not in (-1, 1):
        return HttpResponseBadRequest()
    comment.up_times += int(num)
    comment.save()
    return HttpResponse('%s' % comment.up_times)


class SubCommentCreateView(CreateView):
    "对评论创建回复"
    form_class = SubCommentForm
    template_name = 'subcomment-new.html'
    success_url = ''

    def form_valid(self, form):
        comment_id = self.kwargs.get('comment_id')
        sub = SubComment()
        sub.nickname = form.cleaned_data['nickname']
        sub.email = form.cleaned_data['email']
        sub.content = form.cleaned_data['content']
        sub.related_comment = get_object_or_404(Comment, id=comment_id)
        sub.save()
        if self.request.is_ajax():
            return render_to_response('widgets/comment-new.html',
                                      {'subcomment': sub})
        return HttpResponse('<h4>&nbsp;回复成功！</h4>')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return render_to_response('widgets/form-ajax-invalid.html',
                                      self.get_context_data(form=form))
        return HttpResponse('<h4>回复失败。原因：</h4><p>%s</p>' % form.errors)
