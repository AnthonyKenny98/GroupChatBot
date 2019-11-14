"""Chatbot.py."""

# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-11 13:31:40
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-14 15:04:29

import json
import os
import random
import re
import requests


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

        # Empty stimulus
        self.stimulus = None

        # Load Settings
        self.bravery = float(settings['bravery'])

        # Load Vocabulary
        self.vocab = settings['vocab_path']

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
        self.post_message(self.choose_function()())

    def choose_function(self):
        """Choose a function from a list according to a certain PDF."""
        pos = {
            self.mad_lib: 5,
            self.spongebob_mock: 1,
            self.post_meme: 4
        }
        return random.choice([x for x in pos for y in range(pos[x])])

    def introduce(self):
        """Introduce."""
        return "Hello, my name is {}".format(self.name)

    def mad_lib(self):
        """Return a random mad lib built from vocab."""
        sentence = random.choice(
            self.load_file('/' + self.vocab + '/sentence.txt'))
        placeholders = re.findall(r'@\w+', sentence)
        for placeholder in placeholders:
            sentence = sentence.replace(placeholder, self.word(placeholder), 1)
        return sentence

    def spongebob_mock(self):
        """Return spongebob mock version of message.

        Capitalize every second letter.
        Credit: https://stackoverflow.com/a/17865821
        """
        cap = [True]

        def repl(m):
            cap[0] = not cap[0]
            return m.group(0).upper() if cap[0] else m.group(0).lower()
        return re.sub(r'[A-Za-z]', repl, self.stimulus["message"].text)

    def post_meme(self):
        """Post Meme to Group Chat.

        TODO- clean this up, wrong scope, text should be optional
        """
        attachments = [{
            'type': 'image',
            'url': self.user.upload_photo(self.get_meme())
        }]
        self.post_message('', attachments=attachments)

    def word(self, word_type):
        """Return list of options for a given word_type."""
        if word_type == '@tag_member':
            return self.tag_member()
        else:
            return random.choice(
                self.load_file('/{}/{}.txt'.format(self.vocab, word_type[1:])))

    @staticmethod
    def load_file(file):
        """Load txt file into array and return."""
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + file, 'r') as f:
            array = f.read().splitlines()
        return array

    @staticmethod
    def decision_true(probability=0.5):
        """Return True with given probability."""
        return random.random() < probability

    @staticmethod
    def get_meme():
        """Return Binary Image Data of a Meme."""
        # s = 'me_irl'
        s = 'cursedImages'
        meme_url = requests.get(
            "https://meme-api.herokuapp.com/gimme/{}".format(s)).json()['url']
        return requests.get(meme_url).content
