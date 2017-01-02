# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2017-01-02 12:29:29
# @Last Modified by:   Michael
# @Last Modified time: 2017-01-02 15:27:18
import pytest
import json

from source import HTTPListener


@pytest.fixture
def client():
    HTTPListener.app.config['TESTING'] = True
    app = HTTPListener.app.test_client()

    return app


def create(client, reponame, url):
    return client.get('/create?reponame=%s&url=%s' % (reponame, url), follow_redirects=True)


def update(client, reponame):
    return client.get('/update?reponame=%s' % reponame, follow_redirects=True)


def delete(client, reponame):
    return client.get('/delete?reponame=%s' % reponame, follow_redirects=True)


def test_create(client):
    """
    @brief      test create repo API.
    """
    rv = create(client, reponame='Michael', url='https://github.com/Michael')
    assert json.loads(rv.data.decode())['code'] == 0
    assert json.loads(rv.data.decode())['owner'] == 'Michael'
    assert json.loads(rv.data.decode())['url'] == 'https://github.com/Michael'


def test_update(client):
    """
    @brief      test update repo API.
    """
    rv = update(client, 'Michael')
    assert json.loads(rv.data.decode())['code'] == 0
    assert json.loads(rv.data.decode())['owner'] == 'Michael'


def test_delete(client):
    """
    @brief      test delete repo API.
    """
    rv = delete(client, 'Michael')
    assert json.loads(rv.data.decode())['code'] == 0
    assert json.loads(rv.data.decode())['owner'] == 'Michael'
