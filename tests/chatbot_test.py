"""ChatBot Tests."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-11 21:49:10
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-12 17:53:26

from src.chatbot import ChatBot


def test_init():
    """Test Initialization of ChatBot."""
    c = ChatBot()

    # self.bravery
    assert type(c.bravery) is float
    assert c.bravery <= 1
    assert c.bravery >= 0


def test_post_message():
    """Test is void."""
    c = ChatBot()

    assert c.post_message() is None


def test_api_pre_react_checks():
    """Test is void."""
    c = ChatBot()

    assert c.api_pre_react_checks() is None


def test_tag_member():
    """Test is void."""
    c = ChatBot()

    assert c.tag_member() is None


def test_react():
    """TODO."""
    pass


def test_introduce():
    """Test func returns correct string."""
    c = ChatBot()
    c.name = "Test"

    assert type(c.introduce()) == str
    assert c.introduce() == "Hello, my name is {}".format(c.name)


def test_mad_lib():
    """TODO."""
    """Test func returns correct string."""
    # c = ChatBot()
    # c.stimulus["message"] = Message()

    # assert type(c.insult()) == str
    # assert '@tag_member' not in c.insult()
    # assert '@noun' not in c.insult()
    # assert '@adjective' not in c.insult()


def test_word_options():
    """TODO."""
    pass


def test_load_file():
    """Test static method returns list."""
    assert type(ChatBot.load_file('/vocab/default.noun')) is list
    assert len(ChatBot.load_file('/vocab/default.noun')) > 0


def test_decision_true():
    """Test static method returns bool."""
    assert type(ChatBot.decision_true()) is bool
