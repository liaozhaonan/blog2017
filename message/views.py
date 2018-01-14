from django.shortcuts import Http404, render_to_response
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.conf import settings

from .models import Message
from .forms import MessageForm
# Create your views here.


class MessageView(ListView):
    "留言版页面视图"
    context_object_name = 'messages'
    paginate_by = settings.PAGE_NUM

    def get_template_names(self):
        if self.request.is_ajax():
            return 'widgets/message-list.html'
        return 'messages.html'

    def get_queryset(self):
        types = self.request.GET.get('types', '')
        if not types:
            types = 'all'

        # 如果types为all, 返回所有留言, 否则返回对应类型(programming/others)的留言
        if types == 'all':
            messages = Message.objects.all()
        elif types == 'programming':
            messages = Message.objects.filter(types='P')
        elif types == 'others':
            messages = Message.objects.filter(types='O')
        else:
            raise Http404

        return messages


class MessageCreateView(CreateView):
    "创建留言"
    form_class = MessageForm
    template_name = 'messages.html'

    def get_success_url(self):
        if self.request.is_ajax():
            return '/message/ajax-success/'
        return '/messages/'

    def form_invalid(self, form):
        if self.request.is_ajax():
            return render_to_response('widgets/form-ajax-invalid.html',
                                      self.get_context_data(form=form))
        return self.render_to_response(self.get_context_data(form=form))


def message_ajax_success(request):
    "异步创建留言成功后跳转到该视图"
    message = Message.objects.first()  # 获取刚创建的留言
    return render_to_response('widgets/message-ajax-success.html',
                              {'message': message})
