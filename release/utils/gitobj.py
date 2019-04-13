# 获取git分支
# 获取分支的提交信息
# 获取所有的tag
# 根据分支+提交信息更新
# 根据tag更新
import os
from git import Repo, Git
import subprocess

class GitObj(object):
    def __init__(self, path):
        # path: 本地git文件仓库(初始化git根目录上一层, 项目根目录)
        self.path = os.path.join("/update/git", path)
        # self.path = path

    def is_gitdir(self, url):  # 本地仓库是否存在,不存在在创建
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        path = os.path.join(self.path, '.git')
        if os.path.isdir(path):  # 仓库存在本地
            return True
        else:  # 仓库未创建
            Repo.clone_from(url, self.path)
            return False

    def branches(self):  # 获取分支信息
        return [str(b).split('/')[1] for b in Repo(self.path).remote().refs if str(b) != "origin/HEAD"]

    def tags(self):  # 获取 版本
        return [str(b) for b in Repo(self.path).tags]

    def checkout(self, branch):  # 分支切换
        ab = Repo(self.path).active_branch  # 获取当前的分支名称
        subprocess.getoutput("cd {} && git reset --hard origin/{}".format(self.path, ab))  # 强制将本地分支与远程分支同步
        Git(self.path).checkout(branch)  # 切换分支, 本地不存在,远程仓库必须有

    def commits(self, branch):  # 获取提交过的版本
        self.checkout(branch)
        return [{'message': commit.message, "id": commit.hexsha} for commit in Repo(self.path).iter_commits()]

    def update_version(self, branch, utype, commit=None):
        self.checkout(branch)
        if utype != "tag":
            Repo(self.path).index.reset(commit=commit, head=True)
