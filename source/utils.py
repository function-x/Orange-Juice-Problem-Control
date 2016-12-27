# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 03:34:39
# @Last Modified by:   Michael
# @Last Modified time: 2016-12-27 16:18:25
import git
import json
import os


class GitEngine(object):
    """
    @brief      Drive of git.
    """
    def __init__(self, root):
        super(GitEngine, self).__init__()
        self.root = root
        self.ownerRepos = {}  # 这个数据结构用于保存(submodule, last push binsha)键值对，日后我会把他保存在文件里
        try:
            self.problemHub = git.Repo(root)
            self.readLastCommitBinsha()
        except git.InvalidGitRepositoryError:
            self.setup()
        # self.acrot = git.Actor(author, authorEmaill)

    def updateOwners(self):
        if self.problemHub is None:
            raise UnboundLocalError("didn't init repo.")
        else:
            self.owners = self.problemHub.submodules

    def setup(self):
        self.problemHub = git.Repo.init()

    def readLastCommitBinsha(self):
        with open(os.path.join(self.root, 'LastCommitBinsha.json'), 'r') as fLastCommitBinsha:
            self.ownerRepos = json.loads(fLastCommitBinsha.read())

    def genCurrCommitBinsha(self):
        ownerRepos = {}
        for ownerRepo in self.problemHub.submodules:
            ownerRepos[ownerRepo.name] = ownerRepo.module().head.commit.binsha
        with open(os.path.join(self.root, 'LastCommitBinsha.json'), 'w') as fLastCommitBinsha:
            fLastCommitBinsha.write(json.dumps(ownerRepos))

    def addOnwerRepo(self, owner, url):
        self.problemHub.create_submodule(owner, owner, url=url)

    def update(self, owner):
        ownerRepo = self.problemHub.submodule(owner)
        ownerRepo.update(to_latest_revision=True)
        self.problemHub.git.add(u=True)
        self.problemHub.index.commit("%s from %s is updated." % owner, ownerRepo.url)

    def updateAll(self):
        for ownerRepo in self.problemHub.submodules:
            ownerRepo.update(to_latest_revision=True)

        self.problemHub.git.add(u=True)
        self.problemHub.index.commit("all are updated.")

    def analyzeDiff(self, owner):
        ownerRepo = self.problemHub.submodule(owner)
        for commit in ownerRepo.iter_commits():
            pass
