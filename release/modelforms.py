from release.models import *
from django.forms import ModelForm, ValidationError
from django import forms

__all__ = ['UserProfileForm', ]


class ModelFormCSS(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [field.widget.attrs.update({'class': 'form-control'}) for field in self.fields.values()]


class UserProfileForm(ModelFormCSS):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def clean_email(self):
        if self.instance.pk:  # 如果pk存在,视作用户编辑
            if UserProfile.objects.filter(email=self.cleaned_data['email'].strip()).first().pk != self.instance.pk:
                raise ValidationError('邮箱已经被其他用户使用')
            return self.cleaned_data['email'].strip()
        user = UserProfile.objects.filter(email=self.cleaned_data['email']).first()
        if user:
            raise ValidationError("该邮箱已经存在")
        else:
            return self.cleaned_data['email'].strip()


class HostForm(ModelFormCSS):
    class Meta:
        model = Host
        fields = '__all__'

    def clean_ip_address(self):
        post_ip = self.cleaned_data['ip_address'].strip()
        if self.instance: return post_ip
        if Host.objects.filter(ip_address=post_ip):
            raise ValidationError('IP重复提交')
        return post_ip


class ProjectForm(ModelFormCSS):
    class Meta:
        model = Project
        fields = '__all__'


class CommandForm(ModelFormCSS):
    class Meta:
        model = Command
        fields = '__all__'


class CronForm(ModelFormCSS):
    class Meta:
        model = Cron
        # fields = '__all__'
        exclude = ['time', 'create_user']


class IssueForm(ModelFormCSS):
    class Meta:
        model = Issue
        fields = ["project", 'backup_dir']


class FileForm(ModelFormCSS):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Issue
        fields = ["project", 'backup_dir', 'file_field']
