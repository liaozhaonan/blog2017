from django.conf.urls import url

from .views import CommentCreateView, comment_upvote, SubCommentCreateView


urlpatterns = [
    # Examples:
    # url(r'^$', 'jonah.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^(?P<slug>[0-9a-zA-Z_-]+)/comment-create$',
        CommentCreateView.as_view(), name='comment-create'),
    url(r'^comment/(?P<comment_id>[0-9]+)/upvote/$',
        comment_upvote, name='comment-upvote'),
    url(r'^comment/(?P<comment_id>[0-9]+)/subcomment-create$',
        SubCommentCreateView.as_view(), name='subcomment-create'),
]
