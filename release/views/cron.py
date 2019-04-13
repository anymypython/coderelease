from django.shortcuts import redirect, reverse
from release.modelforms import CronForm
from release.models import Cron
from django.http.response import JsonResponse
from django.template.response import TemplateResponse
from release.utils.pagination import Pagination
from release.utils.ansible2.runner import AdHocRunner
from release.utils.ansible2.inventory import Inventory


def cron_list(request):
    condition = request.GET.get('name', '')
    if request.account.isAdmin == '0':
        cron_obj = Cron.objects.filter(name__contains=condition)
    else:
        cron_obj = Cron.objects.filter(name__contains=condition, create_user=request.account)
    print(cron_obj[0].time)
    pager = Pagination(request.GET.get('page', '1'), cron_obj.count(), request.GET.copy(), 10)
    return TemplateResponse(request, 'cron_list.html',
                            {'page_type': '计划任务', 'all_cron': cron_obj[pager.start: pager.end],
                             'page_html': pager.page_html})


def cron_new(request, pk=0):
    cron_task = Cron.objects.filter(pk=pk).first()
    form = CronForm(instance=cron_task)
    exec_time = form.instance.time.split(" ")
    if request.method == 'POST':
        form = CronForm(instance=cron_task, data=request.POST)
        form.instance.create_user = request.account
        pt = request.POST.getlist('time')
        form.instance.time = " ".join([r.strip() for r in pt])
        if form.is_valid():

            # 计划保存执行计划
            host_data = [{'hostname': h.ip_address, 'ip': h.ip_address, 'port': h.ssh_port} for h in
                         form.cleaned_data["host"]]
            print(host_data)
            ineventory = Inventory(host_data)  # 初始化主机列表
            runner = AdHocRunner(ineventory)  # 执行对象实例化
            # 执行任务初始化
            tasks = [{"action": {"module": 'cron',
                                 "args": "minute={} day={} hour={} month={} weekday={} job={} name={} user={}".format(
                                     pt[0], pt[1], pt[2], pt[3], pt[4], form.cleaned_data['job'],
                                     form.cleaned_data['name'], form.cleaned_data['user']
                                 )}, "name": "crontab"}]
            ret = runner.run(tasks)
            if not ret.results_raw['ok']:
                print(ret.results_raw)
                return JsonResponse({"status": 1, "msg": "添加失败{}".format(ret.results_raw)})
            form.save()
            return JsonResponse({'status': 0, 'msg': '添加计划任务成功'})
        return JsonResponse({'status': -1, 'msg': form.errors})
    if request.path_info.startswith(reverse('croncreate')):
        page_title = "添加计划任务"
    else:
        page_title = "编辑计划任务"
    return TemplateResponse(request, 'cron_new.html',
                            {"page_type": page_title, 'form': form, 'pk': pk, 'tim': exec_time})


def cron_del(request, pk):
    plan = Cron.objects.filter(pk=pk).first()
    host_data = [{'hostname': h.ip_address, 'ip': h.ip_address, 'port': h.ssh_port, } for h in
                 plan.host.all()]
    inventory = Inventory(host_data)
    runner = AdHocRunner(inventory)
    tasks = [
        {"action": {"module": "cron",
                    "args": "name={} user={} state=absent".format(plan.name, plan.user)}, "name": "crontab"}
    ]
    ret = runner.run(tasks)
    plan.delete()

    return JsonResponse({'status': 0, 'msg': '删除成功'})
