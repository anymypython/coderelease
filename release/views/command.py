from release.models import Project, Host, Command
from django.http.response import JsonResponse
from django.template.response import TemplateResponse
from release.utils.pagination import Pagination
from release.utils.ansible2.inventory import Inventory
from release.utils.ansible2.runner import CommandRunner
import datetime
import json
from django.db.models.query import Q


def command(request):
    projects = Project.objects.all()
    return TemplateResponse(request, 'command.html', {'page_type': '远程指令', 'projects': projects})


def commandcreate(request):
    if request.method == 'POST':
        cmd = request.POST.get('command')
        ips = [item.split('(')[0] for item in request.POST.getlist('hosts[]')]
        hosts = Host.objects.filter(ip_address__in=ips)
        host_data = [{'hostname': h.ip_address, 'ip': h.ip_address, 'port': h.ssh_port, } for h in hosts]
        inventory = Inventory(host_data)
        runner = CommandRunner(inventory)
        res = runner.execute(cmd, 'all')
        Command.objects.create(command=cmd, result=json.dumps(res.results_raw), host=json.dumps(ips),
                               user=request.account, create_time=datetime.datetime.now())
        return JsonResponse({'status': 0, 'msg': '命令已执行', 'result': res.results_raw})
    else:
        return JsonResponse({'status': -1, 'msg': '无效的请求'})


# 执行指令历史记录
def executed(request):
    condition = request.GET.get('name', '')
    q = Q()
    q.connector = 'OR'
    q.children.append(('user__username__contains', condition))
    q.children.append(('command__contains', condition))
    q.children.append(('host__contains', condition))
    if request.account.isAdmin == '0':
        form_obj = Command.objects.filter(q)
    else:
        form_obj = Command.objects.filter(user=request.account).filter(q)
    li = []
    for item in form_obj:
        item.host = json.loads(item.host)
        item.command = item.command.split('\n')
        print(item.result)
        item.result = [v for v in json.loads(item.result).values() if v]
        print(item.result)
        # json.loads(item.result.replace("'", '"'))
        li.append(item)
    pager = Pagination(request.GET.get('page', '1'), form_obj.count(), request.GET.copy(), 10)
    return TemplateResponse(request, 'command_list.html',
                            {'form_obj': li[pager.start: pager.end], 'page_html': pager.page_html,
                             'page_type': '执行命令历史'})


def commanddel(request, pk=0):
    Command.objects.filter(pk=pk).delete()
    return JsonResponse({"status": 0, 'msg': '删除成功'})


def command_detail(request, pk):
    detail_com = Command.objects.filter(pk=pk).first()
    # print(detail_com['result'], type(detail_com['result']))
    detail_com.result = json.loads(detail_com.result)
    return TemplateResponse(request, 'commanddetail.html', {'res': detail_com})
