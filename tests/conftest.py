# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2017-01-02 14:45:51
# @Last Modified by:   Michael
# @Last Modified time: 2017-02-07 21:49:09
import pytest
import os
import shutil

from source.gitManager import GitManager


@pytest.fixture()
def git_manager(request):
    os.mkdir('testRepo')
    git_manager = GitManager(root='testRepo', testMode=True)

    def teardown():
        shutil.rmtree('testRepo')
    request.addfinalizer(teardown)

    return git_manager
