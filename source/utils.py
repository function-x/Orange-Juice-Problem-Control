# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 03:34:39
# @Last Modified by:   Michael
# @Last Modified time: 2017-02-08 18:09:52
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
        self.payloads

    def _initParsers(self):
        self.parsers['json'] = JsonPaser()

    def _processDelete(self, files):
        walker = DirWalker()
        walker.appendFiles(files)
        payload = None
        for path, _ in walker:
            payload['problemId'] = getProblemId(path, self.rootPath)
            payload['function'] = 'delete'
            self.payloads.append(payload)

    def _processCU(self, files, owner, isupdate):
        walker = DirWalker()
        walker.appendFiles(files)
        packagePrev = None
        payload = None
        for path, package in walker:
            parser = self.parsers[fileLayoutJudge(path)]
            if packagePrev is None or package != packagePrev:
                packagePrev = package
                payload = parser.parse(path, owner, packagePrev)
            else:
                payload = parser.parse(path, owner, packagePrev)
            if not isupdate:
                payload['problemId'] = getProblemId(path, self.rootPath)
                payload['function'] = 'create'
            else:
                payload['function'] = 'update'
            self.payloads.append(payload)

    def generatePayload(self, changedFiles):
        owner = changedFiles['owner']
        filesToDelete = changedFiles.get('D')
        filesToAdd = changedFiles.get('A')
        filesToUpdate = changedFiles.get('M')
        if filesToDelete is not None:
            self._processDelete(filesToDelete)
        if filesToUpdate or filesToAdd is not None:
            self._processCU(filesToUpdate, owner, True)
        if filesToAdd is not None:
            self._processCU(filesToAdd, owner, False)
        return self.payloads


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
