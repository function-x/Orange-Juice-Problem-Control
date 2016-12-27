# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 02:09:34
# @Last Modified by:   Michael
# @Last Modified time: 2016-12-28 04:58:03
import json
import threading
from .structures import problem_sturcture
from .exceptions import InvalidFileFormatError


class BasePaser(object):
    """
    @brief      The Base paser.
    """
    def __init__(self):
        super(BasePaser, self).__init__()
        self.doneFlag = False
        self.problem = problem_sturcture

    def __repr__(self):
        if self.doneFlag:
            return json.dumps(self.problem)
        else:
            return None

    def parse(self, file, owner, package):
        raise NotImplementedError

    def sign(self, owner, package):
        self.problem['owner'] = owner
        self.problem['package'] = package


class JsonPaser(BasePaser):
    """
    @brief      Class for json paser.
    """
    def __init__(self):
        super(JsonPaser, self).__init__()

    def parse(self, file, *args):
        problem_unprocessed = json.load(open(file, 'r'))

        try:
            self.problem["title"] = problem_unprocessed["title"]
            self.problem["description"] = problem_unprocessed["description"]
            self.problem["type"] = problem_unprocessed["type"]
            self.problem["lable"] = problem_unprocessed["lable"]
        except KeyError as e:
            raise InvalidFileFormatError(e)
        if len(args) != 0:
            self.sign(args)
        self.doneFlag = True

        return self.problem
