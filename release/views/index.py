#coding:utf-8
from django.shortcuts import render, HttpResponse, redirect, reverse
from release import modelforms
from release.models import UserProfile
from django.http.response import JsonResponse
from django.template.response import TemplateResponse
from release.utils.pagination import Pagination


# 用户登陆,首页, 用户增删改查
# Create your views here.

def index(request):
    return TemplateResponse(request, 'index.html', {'page_type': '首页'})


def usercreate(request):
    form_obj = modelforms.UserProfileForm()
    if request.method == 'POST':
        form_obj = modelforms.UserProfileForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return JsonResponse({'status': 0, 'msg': '创建成功'})
        else:
            return JsonResponse({'status': -1, 'msg': list(form_obj.errors.values())[0]})
    return TemplateResponse(request, 'usercreate.html', {'page_type': '创建用户', 'form_obj': form_obj})


def userlist(request):
    condition = request.GET.get('name', '')
    users = UserProfile.objects.filter(username__contains=condition)
    pager = Pagination(request.GET.get('page', '1'), users.count(), request.GET.copy(), 10)
    return TemplateResponse(request, 'user_list.html', {'page_type': '用户列表', 'users': users[pager.start: pager.end],
                                                        'page_html': pager.page_html, })


def usercedit(request, pk=''):
    err_msg = ''
    user = UserProfile.objects.filter(pk=pk).first()
    if request.method == 'POST':
        print(request.POST)
        user_edit = modelforms.UserProfileForm(instance=user, data=request.POST)
        if user_edit.is_valid():
            user_edit.save()
            print('xxx')
            return JsonResponse({'status': 0, 'msg': '修改成功', })
        err_msg = list(user_edit.errors.values())[0]
        print(err_msg)
    if user:
        form_obj = modelforms.UserProfileForm(instance=user)
        return TemplateResponse(request, 'usercreate.html',
                                {'page_type': '编辑用户', 'form_obj': form_obj, 'err_msg': err_msg, 'pk': pk})
    return JsonResponse({'status': 1, 'msg': '用户不存在'})


def userdel(request, pk):
    if UserProfile.objects.filter(pk=pk).delete():
        return redirect(reverse('userlist'))
    else:
        return JsonResponse({'status': -1, 'msg': '用户不存在'})


def login(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserProfile.objects.filter(username=username, password=password).first()
        print(user)
        if user:
            request.session['user_id'] = user.pk
            return redirect(reverse('index'))
        error_msg = '用户或者密码错误'
    return TemplateResponse(request, 'login.html', {'error_msg': error_msg})


def logout(request):
    request.session.flush()
    return redirect(reverse('login'))
