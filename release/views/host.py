from django.shortcuts import  redirect, reverse
from release.modelforms import HostForm
from release.models import Host
from django.http.response import JsonResponse
from django.template.response import TemplateResponse
from release.utils.pagination import Pagination


# 主机展示列表
def hostlist(request):
    condition = request.GET.get('name', '')
    hosts = Host.objects.filter(hostname__contains=condition)
    pager = Pagination(request.GET.get('page', '1'), hosts.count(), request.GET.copy(), 10)
    return TemplateResponse(request, 'host_list.html',
                            {'hosts': hosts[pager.start:pager.end], 'page_html': pager.page_html, 'page_type': '主机列表'})


def hostcreate(request, pk=0):
    form_obj = HostForm()
    err_msg = ''
    user = Host.objects.filter(pk=pk).first()
    print(user, pk)
    if request.method == 'POST':
        form_obj = HostForm(instance=user, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return JsonResponse({'status': 0, 'msg': '操作成功'})
        err_msg = list(form_obj.errors.values())[0]
    if user and request.method == 'GET':
        form_obj = HostForm(instance=user)
    return TemplateResponse(request, 'hostnew.html',
                            {'form_obj': form_obj, 'page_type': '添加主机', 'err_msg': err_msg, 'pk': pk})


def hostdel(request, pk):
    Host.objects.filter(pk=pk).delete()
    return redirect(reverse('hostlist'))
