from django.conf.urls import url
from release.views import index, host, project, command, cron, issue

urlpatterns = [
    url(r'^index/$', index.index, name='index'),
    url(r'^user/list/$', index.userlist, name='userlist'),
    url(r'^user/create/$', index.usercreate, name='usercreate'),
    url(r'^user/edit/(?P<pk>\d+)$', index.usercedit, name='useredit'),
    url(r'^user/del/(?P<pk>\d+)$', index.userdel, name='userdelete'),
    url(r'^host/list/$', host.hostlist, name='hostlist'),
    url(r'^host/create/$', host.hostcreate, name='hostcreate'),
    url(r'^host/edit/(?P<pk>\d+)$', host.hostcreate, name='hostedit'),
    url(r'^host/del/(?P<pk>\d+)', host.hostdel, name='hostdel'),
    url(r'^project/list/$', project.projectlist, name='projectlist'),
    url(r'^project/detail/(?P<pk>\d+)$', project.pro_detail, name='pro_detail'),
    url(r'^project/create/$', project.projectcreate, name='projectcreate'),
    url(r'^project/edit/(?P<pk>\d+)$', project.projectcreate, name='projectedit'),
    url(r'^project/del/(?P<pk>\d+)$', project.projectdel, name='projectdel'),
    url(r'^command/$', command.command, name='command'),
    url(r'^command/detail/(\w+)/$', command.command_detail, name='command_detail'),
    url(r'^command/create$', command.commandcreate, name='commandcreate'),
    url(r'^command/executed$', command.executed, name='executed'),
    url(r'^command/del/(?P<pk>\d+)$', command.commanddel, name='commanddel'),
    url(r'^cron/list$', cron.cron_list, name='cronlist'),
    url(r'^cron/create$', cron.cron_new, name='croncreate'),
    url(r'^cron/edit/(?P<pk>\d+)$', cron.cron_new, name='cronedit'),
    url(r'^cron/del/(?P<pk>\d+)$', cron.cron_del, name='crondel'),
    url(r'^issue/list$', issue.issue_list, name='update_list'),
    url(r'^issue/detail/(?P<pk>\d+)$', issue.issue_detail, name='issue_detail'),
    url(r'^issue/rollback/list$', issue.issue_list, name='rollback_list'),
    url(r'^issue/update/git$', issue.update_git, name='update_git'),
    url(r'^issue/upload/file$', issue.upload_file, name='upload_file'),
    url(r'^issue/rollback/(?P<pk>\d+)$', issue.rollback, name='rollback'),
    url(r'^issue/file/update/test/(?P<pk>\d+)$', issue.file_update, name='file_update_test'),
    url(r'^issue/test/success/(?P<pk>\d+)$', issue.test_success, name='test_success'),
    url(r'^issue/update/all/(?P<pk>\d+)$', issue.update_all, name='update_all'),
    url(r'^get/git/(?P<pk>\d+)/(?P<tp>\w+)/', issue.get_git_info, name="get_git_info"),
    url(r'^get/commits/(?P<pk>\d+)/(?P<bra>\w+)/', issue.commits, name="get_commits")

]
