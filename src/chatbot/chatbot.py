"""Chatbot.py."""

# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-11 13:31:40
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-11 15:01:36


class ChatBot:
    """Provide Parent Class for ChatBot Functionality.

    Is seperate to specific applications.
    """

    def __init__(self, bravery=0.1):
        """Initialize ChatBot."""
        self.name = 'ChatBot Name'
        self.bravery = bravery

    def post_message(self):
        """Send Message as Bot.

        Void method in Parent Class.
        Implemented in Children Classes for specific APIs
        """
        pass

    def api_pre_react_checks(self):
        """Check before going through react logic.

        Void method in Parent Class.
        Implemented in Children Classes for specific APIs
        """
        pass

    def react(self):
        """React to message that awoke the bot."""
        if not self.api_pre_react_checks():
            return
        self.post_message("Test Message")

    def introduce(self):
        """Introduce."""
        return "Hello, my name is {}".format(self.name)
