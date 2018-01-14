from django.conf.urls import url

from message.views import MessageView, message_ajax_success, MessageCreateView


urlpatterns = [
    # Examples:
    # url(r'^$', 'jonah.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', MessageView.as_view(), name='index'),
    url(r'^create/$',
        MessageCreateView.as_view(), name='create'),
    url(r'^ajax-success/$',
        message_ajax_success, name='ajax-success'),
]
