"""Chatbot.py."""

# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-11 13:31:40
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-11 20:51:35

import json
import os
import random


class ChatBot:
    """Provide Parent Class for ChatBot Functionality.

    Is seperate to specific applications.
    """

    def __init__(self):
        """Initialize ChatBot."""
        # Import config settings
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + '/config/default.config', 'r') as f:
            settings = json.load(f)

        # Load Settings
        self.bravery = float(settings['bravery'])

        self.react()

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

    def tag_member(self):
        """Return string that for given API tags groupmember."""
        pass

    def react(self):
        """React to message that awoke the bot."""
        # Execute Logic to decide whether to react
        #   1) Conduct API specific pre-react checks
        if not self.api_pre_react_checks():
            return

        #   2) Always reply if called out
        if self.name not in self.stimulus['message'].text:
            #   3) With probability inversely proportional to bravery setting,a
            #   don't react
            if self.bravery < random.uniform(0, 1):
                return

        # Post response
        self.post_message(self.insult())

    def introduce(self):
        """Introduce."""
        return "Hello, my name is {}".format(self.name)

    def random_phrase(self):
        """Return a random phrase from vocab."""
        return random.choice(self.load_file('/vocab/phrases.txt'))

    def insult(self, tag_member=True):
        """Return a random insult built from vocab."""
        message = ""
        if self.decision_true():
            message += self.tag_member() + ' '
        if self.decision_true():
            message += random.choice(self.load_file('/vocab/preambles.txt')) \
                + ' '
        if self.decision_true():
            message += random.choice(self.load_file('/vocab/adjectives.txt')) \
                + ' '
        message += random.choice(self.load_file('/vocab/nouns.txt'))
        return message

    @staticmethod
    def load_file(file):
        """Load txt file into array and return."""
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + file, 'r') as f:
            list = f.read().splitlines()
        return list

    @staticmethod
    def decision_true(probability=0.5):
        """Return True with given probability."""
        return random.random() < probability
