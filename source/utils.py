# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 03:34:39
# @Last Modified by:   Michael
# @Last Modified time: 2016-12-24 06:15:19
import pygit2
import os
from .exceptions import ResorceNotFoundError


class GitEngine(object):
    """
    @brief      Drive of git.
    """
    def __init__(self, root):
        super(GitEngine, self).__init__()
        self.repo = None
        self.root = root

    def add(self, url, owner, package):
        if owner not in os.listdir(self.root):
            os.mkdir(owner)
        self.repo = pygit2.clone_repository(url=url, path=owner + '/' + package)

    def delete(self, owner, package):
        if owner not in os.listdir(self.root):
            raise ResorceNotFoundError("package onwer %s doesn't exist.")
        os.removedirs(owner + '/' + package)

    def update(self, owner, package):
        self.repo = pygit2.Repository(pygit2.discover_repository(owner + '/' + package))
        pass
        # figure out git auth!
