# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 03:34:39
# @Last Modified by:   Michael
# @Last Modified time: 2017-02-07 21:47:46
import os
import re
import threading
import json
from .parsers import JsonPaser


def fileLayoutJudge(filename):
    return os.path.splitext()[-1].replace('.', '')


def getProblemId(problemPath, root):
    """
    @brief      Gets the problemId.

    @param      problemPath  The problem path
    @param      root         The root

    @return     The problem identifier.
    """
    problemId = None
    with open(os.path.join(root, 'ProblemPath_Id.json'), 'r') as fpath_Id:
        path_id = json.loads(fpath_Id.read())
        problemId = path_id.get(problemPath)
    return problemId


def deleteProblem(problemPath, root):
    """
    @brief      delete the problem.

    @param      problemPath  The problem path
    @param      root         The root path
    """
    path_id = None
    with open(os.path.join(root, 'ProblemPath_Id.json'), 'r+') as fpath_Id:
        path_id = json.loads(fpath_Id.read())
        del path_id[problemPath]
        fpath_Id.seek(0)
        fpath_Id.truncate()
        fpath_Id.write(path_id)


def updateProblemPath(oldPath, newPath, root):
    """
    @brief      update the problem path when problem file's path changed.

    @param      oldPath  The old path
    @param      newPath  The new path
    @param      root     The root path
    """
    with open(os.path.join(root, 'ProblemPath_Id.json'), 'r+') as fpath_Id:
        path_id = json.loads(fpath_Id.read())
        problemId = path_id.get(oldPath)
        del path_id[oldPath]
        path_id[newPath] = problemId
        fpath_Id.seek(0)
        fpath_Id.truncate()
        fpath_Id.write(path_id)


class PayloadGenerator(object):
    """
    @brief      Class for payload generator.
    """
    def __init__(self, rootPath):
        super(PayloadGenerator, self).__init__()
        self.rootPath = rootPath
        self.parsers = dict()
        self.initParsers()
        self.payload_update = list()
        self.payload_add = list()
        self.payload_delete = list()

    def _initParsers(self):
        self.parsers['json'] = JsonPaser()

    def _processDelete(self, files):
        walker = DirWalker()
        walker.appendFiles(files)
        for path, _ in walker:
            self.payload_delete['problemId'] = getProblemId(path, self.rootPath)

    def _processUpdate(self, files, owner, payloads):
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

    def generatePayload(self, changedFiles):
        owner = changedFiles['owner']
        filesToDelete = changedFiles.get('D')
        filesToAdd = changedFiles.get('A')
        filesToUpdate = changedFiles.get('M')
        if filesToDelete is not None:
            self._processDelete(filesToDelete)
        if filesToUpdate is not None:
            self._processUpdate(filesToUpdate, owner, self.payload_update)
        if filesToAdd is not None:
            self._processUpdate(filesToUpdate, owner, self.payload_add)


class DirWalker(object):
    """
    @brief      modified file path traveller.
    """
    def __init__(self):
        super(DirWalker, self).__init__()
        self.fileList = []
        self.lock = threading.Lock()

    def appendFiles(self, files):
        with self.lock:
            self.fileList += files
            self.fileList = sorted(set(self.fileList), key=self.fileList.index)

    def analysePacakge(self, path):
        return re.compile(r'.*?/').findall(path)[-1][:-1]

    def walk(self):
        index = 0
        while self.fileList:
            path = self.fileList.pop(index)
            yield path, self.analysePacakge(path)
