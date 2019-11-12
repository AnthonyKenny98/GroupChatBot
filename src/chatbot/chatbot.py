"""Chatbot.py."""

# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-11 13:31:40
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-11 20:16:24

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
        # Conduct API specific pre-react checks
        if not self.api_pre_react_checks():
            return

        # With probability inversely proportional to bravery setting,a
        # don't react
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

    def insult(self):
        """Return a random insult built from vocab."""
        noun = random.choice(self.load_file('/vocab/nouns.txt'))
        adjective = random.choice(self.load_file('/vocab/adjectives.txt'))
        preamble = random.choice(self.load_file('/vocab/preambles.txt'))
        return self.tag_member() + ' ' + preamble + ' ' + adjective \
            + ' ' + noun

    @staticmethod
    def load_file(file):
        """Load txt file into array and return."""
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + file, 'r') as f:
            list = f.read().splitlines()
        return list
