# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 03:34:39
# @Last Modified by:   Michael
# @Last Modified time: 2016-12-28 04:51:17
import git
import json
import os
import re
from collections import defaultdict


def fileLayoutJudge(filename):
    return os.path.splitext()[-1].replace('.', '')


class DirWalker(object):
    """
    @brief      modified file path traveller.
    """
    def __init__(self):
        super(DirWalker, self).__init__()
        self.fileList = []

    def appendFiles(self, files):
        self.fileList += files
        self.fileList = sorted(set(self.fileList), key=self.fileList.index)

    def analysePacakge(self, index):
        return re.compile(r'.*?/').findall(self.fileList[index])[-1][:-1]

    def walk(self, index=0):
        while self.fileList:
            yield self.fileList.pop(index), self.analysePacakge(index)


class GitManager(object):
    """
    @brief      Drive of git.
    """
    def __init__(self, root):
        super(GitManager, self).__init__()
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
        self._addAndCommit(self.problemHub, "owner %s's repo from %s is created." % owner, url)

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
        self._addAndCommit(self.problemHub, "owner %s's repo is deleted." % owner)

    def analyzeDiff(self, owner):
        commit = self._getLastCommit(owner)
        diffs = commit.diff(self.ownerRepo.head.commit)  # 有可能用户会执行mv A B这样的命令，会无端增加操作数量，此处有优化空间
        changedFiles = defaultdict(list)
        changedFiles['owner'] = owner
        for diff in diffs:
            if diff.change_type == 'D':
                changedFiles['D'].append(os.path.join(self.problemHub.working_dir, os.path.join(owner, diff.b_path)))
            elif diff.change_type == 'A' or 'M':
                changedFiles['A'].append(os.path.join(self.problemHub.working_dir, os.path.join(owner, diff.b_path)))
            else:
                changedFiles['D'].append(os.path.join(self.problemHub.working_dir, os.path.join(owner, diff.b_path)))
                changedFiles['A'].append(os.path.join(self.problemHub.working_dir, os.path.join(owner, diff.b_path)))
                # 此处可优化
        return changedFiles
