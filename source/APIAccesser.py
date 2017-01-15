# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2017-01-14 19:46:39
# @Last Modified by:   Michael
# @Last Modified time: 2017-01-16 03:42:08
from requests import session
import json


class Accesser(object):
    """
    @brief      API accesser for update user repo changes.
    """
    def __init__(self, domain):
        super(Accesser, self).__init__()
        self.domain = domain
        self.session = session()  # maybe import from user.
        self.response = None

    def create(self, payload):
        self.response = self.session.post(self.domain + '/problem', data=payload)
        if self.response.status_code != 200:
            return None
        return json.loads(self.response.text)

    def update(self, payload, problemId):
        payload['problemId'] = problemId
        self.response = self.session.put(self.domain + '/problem', data=payload)
        if self.response.status_code != 200:
            return False
        return True

    def delete(self, problemId):
        payload = dict()
        payload['problemId'] = problemId
        self.response = self.session.delete(self.domain + '/problem', data=payload)
        if self.response.status_code != 200:
            return False
        return True
