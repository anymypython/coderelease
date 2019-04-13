from django.db import models

# 项目开发语言
language = (("0", 'Java'), ('1', 'python'), ('2', 'PHP'), ('3', 'HTML'), ('4', 'Go'))
# host-issue发布状态
status = (
    ("0", "等待更新"),
    ("1", "更新中"),
    ("2", "等待测试"),
    ("3", "测试通过"),
    ("4", "更新完成"),
    ("5", "更新失败"),
    ("6", "回滚成功"),
)

env = (
    ("0", '开发'),
    ("1", "测试"),
    ("2", "准生产"),
    ("3", "生产")
)


class Host(models.Model):
    hostname = models.CharField(verbose_name="主机名", max_length=64)
    ip_address = models.GenericIPAddressField(verbose_name="IP地址")
    type = models.CharField(verbose_name='类型', choices=(("0", 'nginx'), ("1", 'other')), max_length=12)
    ssh_port = models.PositiveIntegerField(verbose_name='SSH端口号')
    settings = models.CharField(verbose_name='环境', choices=env, default="0", max_length=20)

    def __str__(self):
        return self.hostname


class UserProfile(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=64, unique=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    email = models.EmailField(verbose_name="电子邮箱", unique=True)
    phone = models.BigIntegerField(verbose_name='手机号码', unique=True)
    role = models.CharField(verbose_name='用户角色', max_length=12, choices=(('0', '开发'), ('1', '测试'), ('2', '运维')),
                            default='0')
    department = models.CharField(verbose_name='所属部门', max_length=32, choices=(('0', '研发'), ('1', '测试'), ('2', '运维')))
    isAdmin = models.CharField(verbose_name='管理员', choices=(("0", "Admin"), ("1", "普通")), default="1",
                               max_length=10)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.username


class Project(models.Model):
    name = models.CharField(verbose_name="项目名称", max_length=64, unique=True)
    create_time = models.DateField(verbose_name="创建时间", auto_created=True, blank=True, auto_now_add=True)
    dev = models.ManyToManyField(verbose_name="研发人员", related_name='dev_user', to='UserProfile')
    test = models.ManyToManyField(verbose_name='测试人员', related_name='test_user', to='UserProfile')
    path = models.CharField(verbose_name='项目目录', max_length=200)
    git_repo = models.CharField(verbose_name="Git仓库", max_length=64)
    host = models.ManyToManyField(verbose_name='使用主机', to='Host', related_name='pro')
    note = models.CharField('项目介绍', blank=True, null=True, default=None, max_length=2000)
    Language = models.CharField(verbose_name='语言', max_length=12, choices=language)
    nginx_host = models.ManyToManyField(verbose_name='Nginx主机', to='Host', related_name='nginx_hosts')
    nginx_conf = models.CharField('nginx配置', blank=True, null=True, max_length=200)
    nginxupstream = models.CharField(verbose_name='nginx upstream名称', max_length=200, null=True, blank=True)
    domain_name = models.CharField('域名', blank=True, null=True, max_length=128)

    class Meta:
        ordering = ["-create_time", ]

    def __str__(self):
        return self.name


class Command(models.Model):
    command = models.CharField('指令', max_length=512)
    result = models.TextField(verbose_name='执行结果')
    host = models.CharField(verbose_name="执行主机", max_length=2000)
    user = models.ForeignKey(verbose_name='执行用户', to='UserProfile')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        ordering = ('-create_time',)

    def __str__(self):
        return self.command


class Cron(models.Model):
    name = models.CharField(verbose_name='计划任务名称', max_length=128)
    note = models.CharField(verbose_name="计划描述", null=True, blank=True, max_length=256)
    time = models.CharField(verbose_name='计划任务执行的时间', max_length=64)  # 分时日月周
    job = models.CharField(verbose_name="计划", max_length=64)
    user = models.CharField(verbose_name='执行用户', max_length=64, default='root')
    host = models.ManyToManyField(to='Host', related_name="cron")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    create_user = models.ForeignKey(UserProfile, verbose_name="创建者")

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class Issue(models.Model):
    project = models.ForeignKey(verbose_name='项目名称', to='Project', related_name='project')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    release_user = models.ForeignKey(verbose_name='发布人', to='UserProfile')
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    status = models.CharField(verbose_name='发布状态', choices=status, max_length=12)
    backup = models.CharField(verbose_name='是否备份', choices=(('0', 'yes'), ('1', 'no')), max_length=20)
    backup_dir = models.CharField(verbose_name='备份路径', max_length=128)
    type = models.CharField(verbose_name='更新类型', max_length=12, choices=(('0', '文件'), ('1', 'git')))
    src_path = models.CharField(verbose_name='上传文件路径', max_length=1024, null=True, blank=True)


class HostIssue(models.Model):
    project = models.ForeignKey('Project', verbose_name='发布项目')
    user = models.ForeignKey('UserProfile', verbose_name='发布人', max_length=20)
    # 每个机器一个发布信息
    host = models.ForeignKey('Host', verbose_name='发布机器')
    issue = models.ForeignKey('Issue', verbose_name='更新')
    # auto_now_add创建时写入时间, auto_now: 每次更新记录都会记录新的时间
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_date = models.DateTimeField('更新时间', auto_now=True)
    type = models.CharField(verbose_name='更新类型', choices=(('0', '文件'), ('2', 'git')), max_length=20)
    status = models.CharField(verbose_name='更新状态', choices=status, default='0', max_length=20)
    backup = models.CharField(verbose_name='备份状态', choices=((0, '是'), (1, '否')), default=0, max_length=20)

    class Meta:
        ordering = ['-create_time']


class Test(models.Model):
    url = models.CharField(verbose_name='url', max_length=200)
    binfa = models.CharField(verbose_name='并发数', max_length=200)
    num = models.CharField(verbose_name='次数', max_length=2000)
    all_num = models.CharField(verbose_name='完成总次数请求', max_length=2000)
    success_rate = models.CharField(verbose_name='成功率', max_length=2000)
    alltime = models.CharField(verbose_name='总用时', max_length=2000)
    data = models.CharField(verbose_name='传输数据', max_length=2000)
    response = models.CharField('响应时间', max_length=2000)
    rate = models.CharField(verbose_name='平均每秒完成的请求', max_length=2000)
    throughput = models.CharField(verbose_name='每秒传输的数据', max_length=2000)
    concurrent = models.CharField(verbose_name='实际最高并发连接数', max_length=2000)
    successful = models.CharField(verbose_name='成功次数', max_length=2000)
    failed = models.CharField(verbose_name='失败次数', max_length=2000)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
