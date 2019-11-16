"""Test functions for groupme.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 14:58:25
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-16 15:25:08

import os
import pytest

from src.groupme import GroupMeChatBot
from src.message import Message

TEST_DATA = {
    'attachments': [],
    'avatar_url': 'https://i.groupme.com/ \
        750x750.jpeg.b5c60559b63741f39f499aec0f171cf0',
    'created_at': 1573493995,
    'group_id': '55604032',
    'id': '157349399548016936',
    'name': 'Anthony Kenny',
    'sender_id': '41327836',
    'sender_type': 'user',
    'source_guid': '5719AB7F-D7C2-4523-B665-14D6DCE91DE6',
    'system': False,
    'text': 'Test Message',
    'user_id': '41327836'
}


@pytest.mark.skipif('TRAVIS' in os.environ, reason='No GroupMe Access Token')
def test_init():
    """Test Initialization of ChatBot."""
    g = GroupMeChatBot(TEST_DATA)

    # self.bravery
    assert type(g.settings['bravery']) is float
    assert g.settings['bravery'] <= 1
    assert g.settings['bravery'] >= 0

    # self.stimulus
    assert g.stimulus is not None

    # self.vocab
    assert g.vocab is not None


@pytest.mark.skipif('TRAVIS' in os.environ, reason='No GroupMe Access Token')
def test_post_message():
    """TODO."""
    pass


@pytest.mark.skipif('TRAVIS' in os.environ, reason='No GroupMe Access Token')
def test_pre_react_checks():
    """Test is bool."""
    g = GroupMeChatBot(TEST_DATA)

    assert type(g.pre_react_checks()) is bool


@pytest.mark.skipif('TRAVIS' in os.environ, reason='No GroupMe Access Token')
def test_tag_member():
    """Test tags member correctly."""
    g = GroupMeChatBot(TEST_DATA)

    assert type(g.tag_member()) is str
    assert g.tag_member()[0] == '@'


@pytest.mark.skipif('TRAVIS' in os.environ, reason='No GroupMe Access Token')
def test_react():
    """TODO."""
    pass


@pytest.mark.skipif('TRAVIS' in os.environ, reason='No GroupMe Access Token')
def test_introduce():
    """Test func returns correct string."""
    g = GroupMeChatBot(TEST_DATA)
    g.name = "Test"

    assert type(g.introduce()) == Message
    assert g.introduce().text == "Hello, my name is {}".format(g.name)


@pytest.mark.skipif('TRAVIS' in os.environ, reason='No GroupMe Access Token')
def test_mad_lib():
    """Test func returns correct string."""
    g = GroupMeChatBot(TEST_DATA)

    assert type(g.mad_lib()) == Message
    assert '@member' not in g.mad_lib().text
    assert '@noun' not in g.mad_lib().text
    assert '@adjective' not in g.mad_lib().text


def test_load_file():
    """Test static method returns list."""
    # assert type(GroupMeChatBot.load_file('/vocab/default/noun.txt')) is list
    # assert len(GroupMeChatBot.load_file('/vocab/default/noun.txt')) > 0
    pass
