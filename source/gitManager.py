# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2017-02-07 21:46:35
# @Last Modified by:   Michael
# @Last Modified time: 2017-02-07 21:48:21
import os
import git
import json
from collections import defaultdict
from .exceptions import ResorceNotFoundError
from .utils import updateProblemPath


class GitManager(object):
    """
    @brief      Drive of git.
    """
    def __init__(self, root, testMode=False):
        super(GitManager, self).__init__()
        self.root = root
        self.commitTable = {}  # 这个数据结构用于保存(submodule, last push hexsha)键值对
        self.ownerRepo = None
        try:
            self.problemHub = git.Repo(root)
            self.readLastCommitHexsha()
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
            if self.commitTable[owner] == commit.hexsha:
                return commit

    def readLastCommitHexsha(self):
        with open(os.path.join(self.root, 'LastCommitHexsha.json'), 'r') as fLastCommitHexsha:
            self.commitTable = json.loads(fLastCommitHexsha.read())

    def genCurrCommitHexsha(self):
        # separate each repo
        ownerRepos = {}
        for ownerRepo in self.problemHub.submodules:
            ownerRepos[ownerRepo.name] = ownerRepo.module().head.commit.hexsha
        with open(os.path.join(self.root, 'LastCommitHexsha.json'), 'w') as fLastCommitHexsha:
            fLastCommitHexsha.write(json.dumps(ownerRepos))

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
        self.genCurrCommitHexsha()
        self._setOwnerRepo(owner)
        self.ownerRepo.update(to_latest_revision=True)
        self._addAndCommit(self.problemHub, "%s from %s is updated." % (owner, self.ownerRepo.url))

    def updateAllOnwerRepo(self):
        self.genCurrCommitHexsha()
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
        diffs = commit.diff(self.ownerRepo.head.commit)
        changedFiles = defaultdict(list)
        for diff in diffs:
            if diff.change_type == 'D':
                changedFiles['D'].append(os.path.join(self.problemHub.working_dir, os.path.join(owner, diff.b_path)))
            elif diff.change_type == 'A':
                changedFiles['A'].append(os.path.join(self.problemHub.working_dir, os.path.join(owner, diff.b_path)))
            elif diff.change_type == 'M':
                changedFiles['M'].append(os.path.join(self.problemHub.working_dir, os.path.join(owner, diff.b_path)))
            else:
                updateProblemPath(os.path.join(owner, diff.a_path), os.path.join(owner, diff.b_path), self.problemHub.working_dir)
                # Exceptions!!!!!!!!!!
                # 文件目录结构变动不影响数据库条目
        return changedFiles
