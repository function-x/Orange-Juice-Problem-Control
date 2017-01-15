# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-27 19:21:52
# @Last Modified by:   Michael
# @Last Modified time: 2017-01-14 19:45:10
from .utils import fileLayoutJudge, lock, walker
from .parsers import JsonPaser
from collections import defaultdict


class ManageEngine(object):
    """
    @brief      Class for manage engine.
    """
    def __init__(self):
        super(ManageEngine, self).__init__()
        self.parsers = dict()
        self.initParsers()
        self.payloads = defaultdict(list)

    def initParsers(self):
        self.parsers['json'] = JsonPaser()

    def generatePayload(self, changedFiles):
        owner = changedFiles['owner']
        filesToDelete = changedFiles.get('D')
        filesToAdd = changedFiles.get('A')
        filesToUpdate = changedFiles.get('M')
        if filesToDelete is not None:
            self.processDelete(filesToDelete)
        if filesToUpdate is not None:
            self.processUpdate(filesToUpdate, owner, 'M')
        if filesToAdd is not None:
            self.processUpdate(filesToAdd, owner, 'A')

    def processDelete(self, files):
        pass

    def processUpdate(self, files, owner, requestMethod):
        walker.appendFiles(files, lock)
        packagePrev = None
        for path, package in walker:
            parser = self.parsers[fileLayoutJudge(path)]
            if packagePrev is None or package != packagePrev:
                packagePrev = package
                self.payloads[requestMethod].append(parser.parse(path, owner, packagePrev))
            else:
                self.payloads[requestMethod].append(parser.parse(path))
