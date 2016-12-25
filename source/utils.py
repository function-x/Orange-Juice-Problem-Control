# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 03:34:39
# @Last Modified by:   Michael
# @Last Modified time: 2016-12-25 23:38:14
import git


class GitEngine(object):
    """
    @brief      Drive of git.
    """
    def __init__(self, root):
        super(GitEngine, self).__init__()
        self.root = root
        self.problemHub = git.Repo(root)
        self.ownerRepos = self.problemHub.submodules

    def updateOwners(self):
        if self.problemHub is None:
            raise UnboundLocalError("didn't init repo.")
        else:
            self.owners = self.problemHub.submodules

    def setup(self):
        self.problemHub = git.Repo.init()

    def lookup(self):
        self.problemHub = git.Repo(self.root)

    def addOnwerRepo(self, owner, url):
        self.problemHub.create_submodule(owner, owner, url=url)

    def update(self, owner):
        ownerRepo = git.submodule(owner)
        ownerRepo.update(to_latest_revision=True)
        self.problemHub.git.add(u=True)
        self.problemHub.index.commit("%s from %s is updated." % owner, ownerRepo.url)

#
# after all night test..... I got a conclusion is that the package gitpython is poisonous.
# it always add more untracked changes.
# 
# have to explore more to find a wat out using libgit2 which means pygit2.
#
