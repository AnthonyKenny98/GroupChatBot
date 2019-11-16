"""ChatBot Tests."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-11 21:49:10
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-16 14:26:08

from src.chatbot import ChatBot
from src.message import Message


def test_init():
    """Test Initialization of ChatBot."""
    c = ChatBot()

    # self.bravery
    assert type(c.bravery) is float
    assert c.bravery <= 1
    assert c.bravery >= 0

    # self.stimulus
    assert c.stimulus is None

    # self.vocab
    assert c.vocab is not None


def test_post_message():
    """Test is void."""
    c = ChatBot()

    assert c.post_message() is None


def test_pre_react_checks():
    """Test is void."""
    c = ChatBot()

    assert c.pre_react_checks() is None


def test_tag_member():
    """Test is void."""
    c = ChatBot()

    assert c.tag_member() == ""


def test_react():
    """TODO."""
    pass


def test_choose_function():
    """Test returns a class method instance."""
    c = ChatBot()

    assert hasattr(c.choose_function, '__call__')


def test_introduce():
    """Test func returns correct string."""
    c = ChatBot()
    c.name = "Test"

    assert type(c.introduce()) == Message
    assert c.introduce().text == "Hello, my name is {}".format(c.name)


def test_mad_lib():
    """Test func returns correct string."""
    c = ChatBot()
    c.stimulus = Message(sender="TestSender")

    assert type(c.mad_lib()) is Message
    assert '@tag_member' not in c.mad_lib().text
    assert '@noun' not in c.mad_lib().text
    assert '@adjective' not in c.mad_lib().text


def test_spongebob_mock():
    """Test returns string with every second letter capitalized."""
    c = ChatBot()
    c.stimulus = Message(text='this is a test message')

    assert type(c.spongebob_mock()) is Message
    assert c.spongebob_mock().text \
        == "tHiS iS a TeSt MeSsAgE"


def test_load_file():
    """Test static method returns list."""
    # assert type(ChatBot.load_file('/vocab/default/noun.txt')) is list
    # assert len(ChatBot.load_file('/vocab/default/noun.txt')) > 0
    pass


def test_decision_true():
    """Test static method returns bool."""
    assert type(ChatBot.decision_true()) is bool
