# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 03:34:39
# @Last Modified by:   Michael
# @Last Modified time: 2016-12-24 21:04:12
import os
import git
from .exceptions import ResorceNotFoundError


class GitEngine(object):
    """
    @brief      Drive of git.
    """
    def __init__(self, root):
        super(GitEngine, self).__init__()
        self.repo = None
        self.root = root

    def setup(self):
        self.repo = git.Repo.init()

    def lookup(self):
        self.repo = git.Repo(self.root)

    def add(self, owner, url):
        self.repo.create_submodule(owner, owner, url=url)

    def update(self, owner, url):
        pass
