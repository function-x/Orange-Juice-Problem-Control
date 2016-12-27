# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-27 19:21:52
# @Last Modified by:   Michael
# @Last Modified time: 2016-12-28 05:06:36
from .utils import DirWalker, fileLayoutJudge
from .parsers import JsonPaser


def payloadGen(changedFiles):
    owner = changedFiles['owner']
    walker = DirWalker()
    walker.appendFiles(changedFiles['A'])


class ManageEngine(object):
    """
    @brief      Class for manage engine.
    """
    def __init__(self):
        super(ManageEngine, self).__init__()
        pass
