from release.models import Project, HostIssue
from django.http.response import JsonResponse
from django.template.response import TemplateResponse
from release.utils.gitobj import GitObj
from django.db.models.query import Q
from release.models import Issue
from release.modelforms import IssueForm, FileForm
from django.shortcuts import reverse
import time
from django.views.decorators.csrf import csrf_exempt
import os
import random
from release.utils.ansible2.inventory import Inventory
from release.utils.ansible2.runner import AdHocRunner
import openpyxl
from release.utils.pagination import Pagination


def get_git_info(request, pk, tp):
    project = Project.objects.filter(pk=pk).first()
    g = GitObj(project.name)
    data = None
    if tp == 'branches':
        data = g.branches()
    elif tp == 'tags':
        data = g.tags()
    elif tp == 'commits':
        data = g.commits(project.name)
    return JsonResponse({"status": 0, "data": data})


def branches(request, pk):
    project = Project.objects.filter(pk=pk).first()
    g = GitObj(project.name)
    return JsonResponse({"status": 0, 'data': g.branches()})


def tags(request, pk):
    project = Project.objects.filter(pk=pk).first()
    g = GitObj(project.name)
    return JsonResponse({"status": 0, 'data': g.tags()})


def commits(request, pk, bra):
    project = Project.objects.filter(pk=pk).first()
    g = GitObj(project.name)
    return JsonResponse({"status": 0, 'data': g.commits(bra)})


def issue_list(request):
    condition = request.GET.get('table_search', '')
    # Issue.objects.filter(project__test__test_user=)
    if request.path_info == reverse('update_list'):
        page_type = '更新记录'
        all_obj = Issue.objects.filter(
            Q(release_user=request.account) | Q(project__test=request.account),
            project__name__contains=condition)  # Q查询必须放在前面
    else:
        page_type = '回滚记录'
        all_obj = Issue.objects.filter(
            Q(release_user=request.account) | Q(project__test=request.account),
            project__name__contains=condition, status="6")
    pager = Pagination(request.GET.get('page', '1'), all_obj.count(), request.GET.copy(), 10)
    return TemplateResponse(request, 'issue.html', {"page_type": page_type, 'page_html': pager.page_html,
                                                    'all_obj': all_obj[pager.start: pager.end]})


def issue_detail(request, pk):
    issue = Issue.objects.filter(pk=pk).first()
    return TemplateResponse(request, 'issue_detail.html', {"res": issue})


def update_git(request):
    issue_form = IssueForm()
    if request.method == "POST":
        issue_form = IssueForm(data=request.POST)
        issue_form.instance.release_user = request.account
        issue_form.instance.type = "1"
        issue_form.instance.backup_dir = str(int(time.time()))
        if issue_form.is_valid():
            if request.POST.get('utype') == "bra":
                GitObj(issue_form.cleaned_data['project'].name).update_version(request.POST.get('braname'), "bra",
                                                                               request.POST.get('bracommit'))
            else:
                GitObj(issue_form.cleaned_data['project'].name).update_version(request.POST.get('tagname'), "tag")
            issue_form.instance.status = "0"
            iss = issue_form.save()
            host_list = issue_form.cleaned_data['project'].host.all()
            for h in host_list:
                HostIssue.objects.create(host=h, user=request.account, issue=iss,
                                         project=issue_form.cleaned_data['project'], status="0")
            return JsonResponse({'status': 0, 'msg': '添加成功'})
        else:
            return JsonResponse({'status': 1, 'msg': '添加失败{}'.format(issue_form.errors)})
    return TemplateResponse(request, 'git_update.html', {"form": issue_form})


##########文件更新#######################################################################
def handle_uploaded_file(f, pro_name, t):  # 文件保存
    path = "/update/file/{}/{}".format(pro_name, t)  # 文件保存路径
    if not os.path.exists(path):
        os.makedirs(path)
    has_excel = False
    for file in f:
        name = file.name.split(".")[1]  # 获取excel表
        if name in ["xls", "xlsx"]:
            has_excel = True
        with open(os.path.join(path, file.name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    if has_excel:
        for file in f:
            with open(os.path.join(path, file.name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        return True
    else:
        return False


@csrf_exempt
def upload_file(request):  # 文件上传
    form_obj = FileForm()
    if request.method == 'POST':
        form_obj = FileForm(request.POST, request.FILES)  # handle_uploaded_file协助保存文件
        t = str(int(time.time()))  # 生产时间戳str项目备份用
        form_obj.instance.release_user = request.account  # 发布人
        form_obj.instance.type = "0"  # 更新类型: 文件更新
        form_obj.instance.backup_dir = t  # 备份路径
        if form_obj.is_valid():  # 数据有效保存
            pro_obj = form_obj.cleaned_data['project']  # 项目
            form_obj.instance.src_path = "/update/file/{}/{}".format(pro_obj.name, t)  # 文件上传路径
            status = handle_uploaded_file(request.FILES.getlist("file_field"), pro_obj.name, t)  # 调用文件上传接
            form_obj.instance.status = "0"
            issue = form_obj.save()
            host_list = form_obj.cleaned_data['project'].host.all()  # 项目主机
            for h in host_list:  # 项目主机创建更新数据
                HostIssue.objects.create(host=h, issue=issue, user=request.account, status="0",
                                         project=form_obj.cleaned_data['project'])
            if status:  # 文件上传成功
                return JsonResponse({'status': 0, 'msg': '上传成功'})
            else:
                return JsonResponse({'status': 1, 'msg': '上传失败，没有上传excel表格'})
        else:  # 数据无效
            return JsonResponse({'status': 1, 'msg': '添加失败{}'.format(form_obj.errors)})

    return TemplateResponse(request, 'file.html', {'form_obj': form_obj})


def file_update(request, pk):
    issue = Issue.objects.filter(pk=pk).first()  # 发布任务
    host_issue_list = issue.hostissue_set.all()  # 发布项目中所有的主机-发布对象
    # 随机选取一台做发布测试
    rhi = random.choice(host_issue_list)  # 随机抽取一个host_issue对象更新对应主机
    # 从nginx摘下, 更新rhi
    down_res = nginx_romove_host(issue.project, [rhi], 1)
    print(down_res)
    # down_res = True
    host_update_res = update_host([rhi, ], issue, issue.type)
    print(host_update_res)
    if down_res and host_update_res:
        issue.status = "2"
        issue.save()
        rhi.status = "2"
        rhi.save()
        return JsonResponse({'status': 0, 'msg': '更新完成'})
    else:
        issue.status = "5"
        issue.save()
        rhi.status = "5"
        rhi.save()
        return JsonResponse({'status': 1, 'msg': '更新失败'})


def nginx_romove_host(project, hosts, up_down):
    # 下线主机/上线主机
    """
    :param project: 项目
    :param hosts: host_issue对象->>主机
    :param up_down: 上线或者下线   1下线, 0上线
    :return:
    """
    tasks = []
    for ih in hosts:
        if up_down == 1:  # 下线
            tasks.append(
                {"action": {"module": "replace",
                            "args": "path={} regexp=({}.*) replace=#\\1".format(project.nginx_conf,
                                                                                ih.host.ip_address)},
                 "name": "nginx_down"})
        else:
            tasks.append(
                # 把机器上线
                {"action": {"module": "replace",
                            "args": "path={} regexp=#({}.*) replace=\\1".format(project.nginx_conf,
                                                                                ih.host.ip_address)},
                 "name": "nginx_up"},
            )
    # nginx平滑重启
    tasks.append({"action": {"module": "service", "args": "name=nginx state=reloaded"}, "name": "nginx_reload"})
    # 执行任务调用
    host_data = [{'hostname': h.ip_address, 'ip': h.ip_address, 'port': h.ssh_port, } for h in project.nginx_host.all()]
    inventory = Inventory(host_data)
    runner = AdHocRunner(inventory)
    ret = runner.run(tasks)  # 执行任务
    print(ret.results_raw)
    if not ret.results_raw["ok"]:
        return False
    return True


def update_host(hosts, issue, git_file, status=1):
    """:param hosts:  要更新的机器
        :param issue: 当前更新的issue，有文件的地址
        :param git_file: 1 git 2 文件
        :param status 0回滚 1更新
        :return:
    """
    if status == 1:  # 更新
        # 备份文件
        tasks = [
            {"action": {"module": "file",  # 创建备份目录
                        "args": "path=/tmp/{}/{} state=directory".format(issue.project.name, issue.backup_dir)},
             "name": "mkdirsfile"},
            {"action": {"module": "shell",  # 备份文件
                        "args": "cp -rf {} /tmp/{}/{}".format(issue.project.path, issue.project.name,
                                                              issue.backup_dir)}, "name": "backup"}, ]
        if git_file == "1":  # git更新
            tasks.append({"action": {"module": "copy",
                                     "args": "dest={} src=/update/git/{}/".format(issue.project.path,
                                                                                  issue.project.name)},
                          "name": "updategit"})
        else:
            # 更新文件对应表路径
            excel_path = "/update/file/{}/{}/readme.xlsx".format(issue.project.name, issue.src_path)
            if os.path.exists(excel_path):
                wb = openpyxl.load_workbook(excel_path)
                wb1 = wb['replace']
                for r in wb1.rows():
                    tasks.append(
                        {"action": {"module": "copy",
                                    "args": "dest={} src=/update/file/{}/{}/{}".format(
                                        os.path.join(issue.project.path, r[1].value), issue.project.name, issue.path,
                                        r[0].value)},
                         "name": "updatefile"})
            else:
                return False
    else:  # 回滚
        tasks = [{"action": {"module": "shell",
                             "args": "cp -rf /tmp/{}/{} {}".format(issue.project.name, issue.backup_dir,
                                                                   issue.project.path)},
                  "name": "backup"},
                 ]
    host_data = [{'hostname': h.host.ip_address, 'ip': h.host.ip_address, 'port': h.host.ssh_port, } for h in hosts]
    inventory = Inventory(host_data)
    runner = AdHocRunner(inventory)
    ret = runner.run(tasks)
    print(ret.results_raw)
    if not ret.results_raw["ok"]:
        return False
    return True


def test_success(request, pk):
    """ 测试通过 先去获取获取项目
        将机器上线
        将状态改为测试通过
        :param request:
        :param pk:Issue对象pk
        :return:
        """
    test_ok_issue = Issue.objects.filter(pk=pk).first()
    test_host_issue = test_ok_issue.hostissue_set.filter(status="2")  # 获取等待测试的数据
    # 上线nginx下线的测试主机
    nginx_res = nginx_romove_host(test_ok_issue.project, test_host_issue, 1)
    # nginx_res = True
    if nginx_res:
        test_host_issue.update(status="3")  # 将所有查询到的数据都改成测试通过
        wait_issue = test_ok_issue.hostissue_set.filter(status="0")  # 要获取等待更新的数据
        if wait_issue:
            test_ok_issue.status = "3"  # 总表
            test_ok_issue.save()
        # else:
        #     test_ok_issue.status = "4"  # 总表
        #     test_ok_issue.save()
        return JsonResponse({'status': 0, 'msg': '测试通过'})
    else:
        test_ok_issue.status = "5"
        test_ok_issue.save()
        test_host_issue.status = "5"
        test_host_issue.save()
        return JsonResponse({'status': 1, 'msg': '更新失败'})


def rollback(request, pk):  # 回滚
    issue = Issue.objects.filter(pk=pk).first()
    host_issue = issue.hostissue_set.filter(Q(status="2") | Q(status="3"))
    print(host_issue)
    # server_res = True
    server_res = update_host(host_issue, issue, issue.type, 0)
    if server_res:
        issue.status = "6"
        issue.save()
        host_issue.update(status="6")
        return JsonResponse({'status': 0, 'msg': '回滚成功'})
    else:
        issue.status = "7"
        issue.save()
        host_issue.update(status="7")
        return JsonResponse({'status': 1, 'msg': '回滚失败'})


def update_all(request, pk):
    issue = Issue.objects.filter(pk=pk).first()
    host_list = issue.hostissue_set.filter(status="0")
    nginx_res = nginx_romove_host(issue.project, host_list, 1)
    # 更新这台机器的服务(更新所有机器)
    if host_list:
        server_res = update_host(host_list, issue, issue.type)
    else:
        server_res = True
    # 发送邮件，可以通过celery来做
    # nginx_res = True
    # server_res = True
    if nginx_res and server_res:
        issue.status = "2"
        issue.save()
        host_list.update(status="2")
        return JsonResponse({'status': 0, 'msg': '更新完成'})
    else:
        issue.status = "5"
        issue.save()
        host_list.update(status="5")
        return JsonResponse({'status': 1, 'msg': '更新失败'})
