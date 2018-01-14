from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

from blog import views as blog_views, urls as blog_urls
from comment import urls as comment_urls
from message import urls as message_urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', blog_views.HomeView.as_view(), name='home'),
    url(r'^blog/', include(blog_urls, namespace='blog', app_name='blog')),
    url(r'^comment/', include(comment_urls, namespace='comment',
                              app_name='comment')),
    url(r'^message/', include(message_urls, namespace='message',
                              app_name='message')),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'),
        name='about')
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    ]
