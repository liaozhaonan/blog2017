from django.conf.urls import url

from .views import (BlogView, TagView, ArchiveView, SearchView,
                    ArticleView)


urlpatterns = [
    # Examples:
    # url(r'^$', 'jonah.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', BlogView.as_view(), name='index'),
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'^tag/(?P<tag_id>[0-9]{1,2})/$', TagView.as_view(), name='tag'),
    url(r'^archive/(?P<year>20[0-9]{2})/$', ArchiveView.as_view(),
        name='archive'),
    url(r'^article/(?P<slug>[0-9a-zA-Z_-]+)$', ArticleView.as_view(),
        name='article'),
]
