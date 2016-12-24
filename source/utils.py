# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 03:34:39
# @Last Modified by:   Michael
# @Last Modified time: 2016-12-24 18:51:14
import os
from .exceptions import ResorceNotFoundError


class GitEngine(object):
    """
    @brief      Drive of git.
    """
    def __init__(self, root):
        super(GitEngine, self).__init__()
        self.repo = None