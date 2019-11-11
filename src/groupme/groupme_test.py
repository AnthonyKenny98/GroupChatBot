"""Test functions for groupme.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 14:58:25
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-11 12:12:04

from groupme import GroupMe

ACCESS_TOKEN = "TESTACCESSTOKEN"


def test_init():
    """Test Initialization of GroupMe Class."""
    group = GroupMe(ACCESS_TOKEN)
    assert group.baseURL == 'https://api.groupme.com/v3'
    # assert group.headers == {'content-type': 'application/json'}


def test_get_url():
    """Test get_url function returns correct value."""
    group = GroupMe(ACCESS_TOKEN)
    assert group.build_url('messages', groupID='1234') == \
        group.baseURL \
        + "/groups/1234/messages?token=" \
        + ACCESS_TOKEN
