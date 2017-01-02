# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-26 22:06:50
# @Last Modified by:   Michael
# @Last Modified time: 2017-01-02 17:34:41
import pytest
import git
import os

TEST_OWNER = os.environ.get('TEST_OWNER')
TEST_URL = os.environ.get('TEST_URL')


class TestGitManager:
    @pytest.fixture(autouse=True)
    def test_init(self, git_manager):
        git_manager.setup()
        assert type(git_manager.problemHub) is git.repo.base.Repo

    def test_add_repo(self, git_manager):
        git_manager.addOnwerRepo(TEST_OWNER, TEST_URL)

    def test_update_repo(self, git_manager):
        git_manager.addOnwerRepo(TEST_OWNER, TEST_URL)
        git_manager.updateOnwerRepo(TEST_OWNER)

    def test_delete_repo(self, git_manager):
        git_manager.addOnwerRepo(TEST_OWNER, TEST_URL)
        git_manager.removeOnwerRepo(TEST_OWNER)
