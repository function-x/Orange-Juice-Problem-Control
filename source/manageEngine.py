# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-27 19:21:52
# @Last Modified by:   Michael
# @Last Modified time: 2017-01-14 18:55:21
from .utils import fileLayoutJudge, lock, walker
from .parsers import JsonPaser


class ManageEngine(object):
    """
    @brief      Class for manage engine.
    """
    def __init__(self):
        super(ManageEngine, self).__init__()
        self.parsers = dict()
        self.initParsers()
        self.payload = list()

    def initParsers(self):
        self.parsers['json'] = JsonPaser()

    def generatePayload(self, changedFiles):
        owner = changedFiles['owner']
        filesToDelete = changedFiles.get('D')
        filesToUpdate = changedFiles.get('A')
        if filesToDelete is not None:
            self.processDelete(filesToDelete)
        if filesToUpdate is not None:
            self.processUpdate(filesToUpdate, owner)

    def processDelete(self, files):
        pass

    def processUpdate(self, files, owner):
        walker.appendFiles(files, lock)
        packagePrev = None
        for path, package in walker:
            if packagePrev is None or package != packagePrev:
                packagePrev = package
                self.parsers[fileLayoutJudge(path)].parse(path, owner, packagePrev)
            else:
                self.parsers[fileLayoutJudge(path)].parse(path)
