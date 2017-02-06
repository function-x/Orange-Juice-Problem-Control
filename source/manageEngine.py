# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-27 19:21:52
# @Last Modified by:   Michael
# @Last Modified time: 2017-02-07 01:59:54
from .utils import fileLayoutJudge, DirWalker
from .parsers import JsonPaser
from .utils import getProblemId


class ManageEngine(object):
    """
    @brief      Class for manage engine.
    """
    def __init__(self, rootPath):
        super(ManageEngine, self).__init__()
        self.rootPath = rootPath
        self.parsers = dict()
        self.initParsers()
        self.payload_update = list()
        self.payload_add = list()
        self.payload_delete = list()

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
            self.processUpdate(filesToUpdate, owner, self.payload_update)
        if filesToAdd is not None:
            self.processAdd(filesToUpdate, owner, self.payload_add)

    def processDelete(self, files):
        walker = DirWalker()
        walker.appendFiles(files)
        for path, _ in walker:
            self.payload_delete['problemId'] = getProblemId(path, self.rootPath)

    def processUpdate(self, files, owner, payloads):
        walker = DirWalker()
        walker.appendFiles(files)
        packagePrev = None
        problem = None
        for path, package in walker:
            parser = self.parsers[fileLayoutJudge(path)]
            if packagePrev is None or package != packagePrev:
                packagePrev = package
                problem = parser.parse(path, owner, packagePrev)
            else:
                problem = parser.parse(path, owner, packagePrev)
            if payloads is self.payload_update:
                problem['problemId'] = getProblemId(path, self.rootPath)
            payloads.append(problem)
