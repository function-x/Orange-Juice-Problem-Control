# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 03:34:39
# @Last Modified by:   Michael
# @Last Modified time: 2017-01-14 19:46:12
import git
import pickle
import os
import re
import threading
from collections import defaultdict
from .exceptions import ResorceNotFoundError


def fileLayoutJudge(filename):
    return os.path.splitext()[-1].replace('.', '')


class DirWalker(object):
    """
    @brief      modified file path traveller.
    """
    def __init__(self):
        super(DirWalker, self).__init__()
        self.fileList = []

    def appendFiles(self, files, lock):
        with lock:
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
    def __init__(self, root, testMode=False):
        super(GitManager, self).__init__()
        self.root = root
        self.commitTable = {}  # 这个数据结构用于保存(submodule, last push binsha)键值对
        self.ownerRepo = None
        try:
            self.problemHub = git.Repo(root)
            self.readLastCommitBinsha()
        except git.InvalidGitRepositoryError:
            if not testMode:
                self.problemHub = self.setup()
            else:
                pass
        except FileNotFoundError:
            self.commitTable = {}
        # self.acrot = git.Actor(author, authorEmaill)

    # def __str__(self):

    def setup(self, root=None):
        if root is None:
            self.problemHub = git.Repo.init(self.root)
        else:
            self.root = root
            self.problemHub = git.Repo.init(self.root)

    def lookup(self, root=None):
        if root is None:
            self.problemHub = git.Repo(self.root)
        else:
            self.root = root
            self.problemHub = git.Repo(self.root)

    def _setOwnerRepo(self, owner):
        try:
            self.ownerRepo = self.problemHub.submodule(owner)
        except ValueError as e:
            raise ResorceNotFoundError(e)

    def _addAndCommit(self, repo, commitMessage):
        repo.git.add(u=True)
        repo.index.commit(commitMessage)

    def _getLastCommit(self, owner):
        self._setOwnerRepo(owner)
        for commit in self.ownerRepo.iter_commits():
            if self.commitTable[owner] == commit.binsha:
                return commit

    def readLastCommitBinsha(self):
        with open(os.path.join(self.root, 'LastCommitBinsha'), 'rb') as fLastCommitBinsha:
            self.commitTable = pickle.loads(fLastCommitBinsha.read())

    def genCurrCommitBinsha(self):
        # separate each repo
        ownerRepos = {}
        for ownerRepo in self.problemHub.submodules:
            ownerRepos[ownerRepo.name] = ownerRepo.module().head.commit.binsha
        with open(os.path.join(self.root, 'LastCommitBinsha'), 'wb') as fLastCommitBinsha:
            fLastCommitBinsha.write(pickle.dumps(ownerRepos))

    def addOnwerRepo(self, owner, url):
        try:
            for ownerRepo in self.problemHub.submodules:
                if owner == ownerRepo.name:
                    return
        except git.BadName:
            print('no submodule')
        self.problemHub.create_submodule(owner, owner, url=url)
        self._addAndCommit(self.problemHub, "owner %s's repo from %s is created." % (owner, url))

    def updateOnwerRepo(self, owner):
        # separate each repo
        self.genCurrCommitBinsha()
        self._setOwnerRepo(owner)
        self.ownerRepo.update(to_latest_revision=True)
        self._addAndCommit(self.problemHub, "%s from %s is updated." % (owner, self.ownerRepo.url))

    def updateAllOnwerRepo(self):
        self.genCurrCommitBinsha()
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
        """
        @brief      Analyse diff to generate payload and access API.
                    there is one thing to know:
                    git will treat those files who has been modified and
                    renamed as Deleted and Added. so for those files who
                    just renamed doesn't need to track.

        @param      self   The object
        @param      owner  The owner

        @return     a dict of changed files
        """
        commit = self._getLastCommit(owner)
        diffs = commit.diff(self.ownerRepo.head.commit)  # 有可能用户会执行mv A B这样的命令，会无端增加操作数量，此处有优化空间
        changedFiles = defaultdict(list)
        changedFiles['owner'] = owner
        for diff in diffs:
            if diff.change_type == 'D':
                changedFiles['D'].append(os.path.join(self.problemHub.working_dir, os.path.join(owner, diff.b_path)))
            elif diff.change_type == 'A':
                changedFiles['A'].append(os.path.join(self.problemHub.working_dir, os.path.join(owner, diff.b_path)))
            elif diff.change_type == 'M':
                changedFiles['M'].append(os.path.join(self.problemHub.working_dir, os.path.join(owner, diff.b_path)))
            else:
                pass
                # 此处可优化?
        return changedFiles


walker = DirWalker()
lock = threading.Lock()
