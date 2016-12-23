# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 03:34:39
# @Last Modified by:   Michael
# @Last Modified time: 2016-12-24 05:13:10
import pygit2
import os


class GitEngine(object):
    """
    @brief      Drive of git.
    """
    def __init__(self):
        super(GitEngine, self).__init__()
        self.repo = None

    def setup(self, path):
        self.repo = pygit2.init_repository(path)

    def lookup(self, path):
        self.repo = pygit2.Repository(pygit2.discover_repository(path))

    def add(self, url):
        pass
