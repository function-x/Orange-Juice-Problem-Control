# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 03:07:31
# @Last Modified by:   Michael
# @Last Modified time: 2017-02-07 22:08:19


problem_sturcture = {
    "title": None,
    "description": None,
    "package": None,
    "owner": None,
    "type": None,
    "lable": []
}


class Payload(dict):
    """docstring for Payload(dict):"""
    def __init__(self, arg):
        super(Payload, self).__init__()
        self.arg = arg
