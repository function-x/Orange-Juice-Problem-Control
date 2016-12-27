# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 03:34:39
# @Last Modified by:   Michael
# @Last Modified time: 2016-12-27 20:11:09
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
        self.commitTable = {}  # 这个数据结构用于保存(submodule, last push binsha)键值对
        self.ownerRepo = None
        try:
            self.problemHub = git.Repo(root)
            self.readLastCommitBinsha()
        except git.InvalidGitRepositoryError:
            self.problemHub = self.setup()
        except FileNotFoundError:
            self.commitTable = {}
        # self.acrot = git.Actor(author, authorEmaill)

    def __del__(self):
        self.genCurrCommitBinsha()

    # def __str__(self):

    @staticmethod
    def setup():
        git.Repo.init()

    def _setOwnerRepo(self, owner):
        self.ownerRepo = self.problemHub.submodule(owner)

    def _addAndCommit(self, repo, commitMessage):
        repo.git.add(u=True)
        repo.index.commit(commitMessage)

    def _getLastCommit(self, owner):
        self._setOwnerRepo(owner)
        for commit in self.ownerRepo.iter_commits():
            if self.commitTable[owner] == commit.binsha:
                return commit

    def readLastCommitBinsha(self):
        with open(os.path.join(self.root, 'LastCommitBinsha.json'), 'r') as fLastCommitBinsha:
            self.commitTable = json.loads(fLastCommitBinsha.read())

    def genCurrCommitBinsha(self):
        ownerRepos = {}
        for ownerRepo in self.problemHub.submodules:
            ownerRepos[ownerRepo.name] = ownerRepo.module().head.commit.binsha
        with open(os.path.join(self.root, 'LastCommitBinsha.json'), 'w') as fLastCommitBinsha:
            fLastCommitBinsha.write(json.dumps(ownerRepos))

    def addOnwerRepo(self, owner, url):
        self.problemHub.create_submodule(owner, owner, url=url)

    def updateOnwerRepo(self, owner):
        self._setOwnerRepo(owner)
        self.ownerRepo.update(to_latest_revision=True)
        self._addAndCommit(self.problemHub, "%s from %s is updated." % owner, self.ownerRepo.url)

    def updateAllOnwerRepo(self):
        for ownerRepo in self.problemHub.submodules:
            ownerRepo.update(to_latest_revision=True)

        self._addAndCommit(self.problemHub, "all are updated.")

    def removeOnwerRepo(self, owner):
        self._setOwnerRepo(owner)
        try:
            self.ownerRepo.remove(configuration=True)
        except ValueError as e:
            print(e)

    def analyzeDiff(self, owner):
        commit = self._getLastCommit(owner)
        diffs = commit.diff(self.ownerRepo.head.commit)  # 有可能用户会执行mv A B这样的命令，会无端增加操作数量，此处有优化空间
        changedFiles = {}
        changedFiles['owner'] = owner
        for diff in diffs:
            if diff.change_type == 'D':
                changedFiles['D'] = diff.b_path
            elif diff.change_type == 'A' or 'M':
                changedFiles['A'] = diff.b_path
            else:
                pass
        return changedFiles
