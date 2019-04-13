# coding: utf-8
from django.shortcuts import render, HttpResponse, redirect, reverse
from release.modelforms import ProjectForm
from release.models import Project
from django.http.response import JsonResponse
from django.template.response import TemplateResponse
from release.utils.pagination import Pagination
from release.utils.gitobj import GitObj

# 项目展示
def projectlist(request):
    condition = request.GET.get('name', '')
    projects = Project.objects.filter(name__contains=condition)
    pager = Pagination(request.GET.get('page', '1'), projects.count(), request.GET.copy(), 10)
    return TemplateResponse(request, 'project_list.html',
                            {'projects': projects[pager.start:pager.end], 'page_html': pager.page_html,
                             'page_type': '添加项目'})


def pro_detail(request, pk=0):
    pro = Project.objects.filter(pk=pk).first()
    return TemplateResponse(request, 'project_detail.html', {"pro": pro})


def projectcreate(request, pk=0):
    form_obj = ProjectForm()
    err_msg = ''
    user = Project.objects.filter(pk=pk).first()
    if user:
        form_obj = ProjectForm(instance=user)
    if request.method == 'POST':
        form_obj = ProjectForm(instance=user, data=request.POST)
        if form_obj.is_valid():
            GitObj(form_obj.cleaned_data['name']).is_gitdir(form_obj.cleaned_data['git_repo'])
            form_obj.save()
            return JsonResponse({'status': 0, 'msg': '操作成功'})
        err_msg = list(form_obj.errors.values())[0]
        print(err_msg)
    return TemplateResponse(request, 'projectnew.html',
                            {'form_obj': form_obj, 'page_type': '添加项目', 'err_msg': err_msg, 'pk': pk})


def projectdel(request, pk):
    Project.objects.filter(pk=pk).delete()
    return redirect(reverse('projectlist'))
