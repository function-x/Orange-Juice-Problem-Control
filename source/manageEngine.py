# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-27 19:21:52
# @Last Modified by:   Michael
# @Last Modified time: 2017-02-08 17:10:10
from .gitManager import GitManager


class ManageEngine(object):
    """
    @brief      Class for manage engine.
    """
    def __init__(self, rootPath, method):
        super(ManageEngine, self).__init__()
        self.rootPath = rootPath
        self.method = method

    def processRequest(self, method=None):
        self.method = method if method is not None else self.method
        gitManager = GitManager(self.rootPath)
        pass
