"""Chatbot.py."""

# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-11 13:31:40
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-15 09:18:48

import json
import os
import random
import re
import requests

from ..message import Message, Attachment


class ChatBot:
    """Provide Parent Class for ChatBot Functionality.

    Is inherited by application specific ChildChatBot classes.
    """

    def __init__(self, config='/default.config'):
        """Initialize ChatBot.

        Input:
            - config: file name of settings. Format *.config
        Returns:
            Void
        """
        # Import config settings
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + '/config/' + config, 'r') as f:
            settings = json.load(f)

        # Empty stimulus
        self.stimulus = None

        # Load Settings
        self.bravery = float(settings['bravery'])
        self.settings = settings

        # Load Vocabulary
        self.vocab = settings['vocab_path']

    def post_message(self):
        """Send Message as Bot.

        Void method in Parent Class.
        Implemented in Children Classes for specific APIs
        """
        pass

    def pre_react_checks(self):
        """Check before going through react logic.

        Void method in Parent Class.
        Implemented in Children Classes for specific APIs
        """
        pass

    def tag_member(self):
        """Return string that, for given API, tags groupmember.

        Void method in Parent Class.
        Implemented in Children Classes for specific APIs
        """
        return ""

    def react(self):
        """React to message that awoke the bot.

        Input:
            None
        Return:
            Void
        """
        # Execute Logic to decide whether to react

        #   1) Conduct API specific pre-react checks
        if not self.pre_react_checks():
            return

        #   2) Always reply if called out
        if self.name not in self.stimulus.text:
            #   3) With probability inversely proportional to bravery setting,a
            #   don't react
            if self.bravery < random.uniform(0, 1):
                return

        # Post response
        self.post_message(self.choose_function()())

    def choose_function(self):
        """Choose a function from a list according to a certain probability.

        Input:
            None
        Return:
            Class Method Instance
        """
        pdf = self.settings["random_function_call_pdf"]
        funcs = {
            self.mad_lib: int(pdf['mad_lib']),
            self.spongebob_mock: int(pdf['spongebob_mock']),
            self.post_meme: int(pdf['post_meme']),
        }
        return random.choice([x for x in funcs for y in range(funcs[x])])

    def introduce(self):
        """Introduce Self.

        Input:
            None
        Return:
            Message: Introduction
        """
        return Message(
            text='Hello, my name is {}'.format(self.name))

    def mad_lib(self):
        """Return Mad Lib from vocab.

        Input:
            None
        Return
            Message: With completed Mad Lib String
        """
        def word(word_type):
            """Return list of options for a given word_type."""
            return self.tag_member() if word_type == '@tag_member' \
                else random.choice(self.load_file('/{}/{}.txt'.format(
                    self.vocab, word_type[1:])))

        sentence = random.choice(
            self.load_file('/' + self.vocab + '/sentence.txt'))
        placeholders = re.findall(r'@\w+', sentence)
        for placeholder in placeholders:
            sentence = sentence.replace(placeholder, word(placeholder), 1)
        return Message(text=sentence)

    def spongebob_mock(self):
        """Capitalize every second letter.

        Credit: https://stackoverflow.com/a/17865821

        Input:
            None
        Return:
            Message: With alternating capitalized version of self.stimulus.text
        """
        cap = [True]

        def repl(m):
            cap[0] = not cap[0]
            return m.group(0).upper() if cap[0] else m.group(0).lower()
        return Message(
            text=re.sub(r'[A-Za-z]', repl, self.stimulus.text))

    def post_meme(self):
        """Post Meme.

        Input:
            None
        Return:
            Message: Empty string and list of one attachment = [<meme>]
        """
        attachments = [Attachment(
            type='image',
            url=self.user.upload_photo(
                self.get_meme(self.settings['subreddits']))
        )]
        message = Message(attachments=attachments)
        return message

    @staticmethod
    def load_file(file):
        """Load txt file into array and return.

        Input:
            String: File path relative to chatbot.py
        Return:
            String Array: Lines of file
        """
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + file, 'r') as f:
            array = f.read().splitlines()
        return array

    @staticmethod
    def decision_true(probability=0.5):
        """Return True with given probability."""
        return random.random() < probability

    @staticmethod
    def get_meme(subs):
        """Return Binary Image Data of a Meme.

        Input:
            None
        Return:
            Binary Image Data of Picture
        """
        s = random.choice([x for x in subs for y in range(int(subs[x]))])
        meme_url = requests.get(
            'https://meme-api.herokuapp.com/gimme/{}'.format(s)).json()['url']
        return requests.get(meme_url).content
