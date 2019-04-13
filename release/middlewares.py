#coding:utf-8
from django.middleware.http import MiddlewareMixin
from django.shortcuts import reverse, redirect
from release.models import UserProfile


class LoginMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info.startswith('/admin/'):
            return
        if request.path_info in [reverse('login'), ]:
            return
        user_id = request.session.get('user_id', -1)
        user = UserProfile.objects.filter(pk=user_id).first()
        if user:
            request.account = user
        else:
            return redirect(reverse('login'))


class TemplateRes(MiddlewareMixin):
    def process_template_response(self, request, response):
        # 获取response的数据(orderdict)
        if hasattr(request, 'account'):
            response.context_data.update({'user': request.account})
        return response
