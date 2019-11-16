"""Chatbot.py."""

# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-11 13:31:40
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-16 14:25:29

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

    def __init__(self, config=None):
        """Initialize ChatBot.

        Input:
            - config: file name of settings. Format *.config
        Returns:
            Void
        """
        if config is None:
            config = 'default'
        # Import config settings
        self.path = os.path.dirname(os.path.realpath(__file__))
        with open(self.path + '/config/' + config + '.config', 'r') as f:
            self.settings = json.load(f)

        # Empty stimulus
        self.stimulus = None

        # Load Settings
        self.bravery = float(self.settings['bravery'])

        # Load Vocabulary
        self.vocab = {}
        path = '{}/vocab/{}/'.format(self.path, self.settings['vocab'])
        for file in filter(lambda f: f.endswith('.txt'), os.listdir(path)):
            self.vocab[file.replace('.txt', '')] = self.load_file(path + file)

    def post_message(self):
        """Send Message as Bot."""
        pass

    def pre_react_checks(self):
        """Check before going through react logic."""
        pass

    def tag_member(self, reply=False):
        """Return string that, for given API, tags groupmember."""
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
        if self.name.lower() not in self.stimulus.text.lower():
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
            self.cross_map: int(pdf['cross_map']),
            self.create_meme: int(pdf['create_meme'])
        }
        return random.choice([x for x in funcs for y in range(funcs[x])])

    def introduce(self):
        """Return Message Object with introduction."""
        return Message(
            text='Hello, my name is {}'.format(self.name))

    def mad_lib(self, reply=True):
        """Return Mad Lib from vocab.

        Input:
            None
        Return
            Message: With completed Mad Lib String
        """
        def pick_sentence():
            return random.choice(self.vocab['sentence'])
        sentence = pick_sentence()

        while not reply and '@tag_member' not in sentence:
            sentence = pick_sentence()

        sentence = sentence.replace('@member', self.tag_member(reply=True))
        return Message(text=self.sub_placeholders(sentence))

    def sub_placeholders(self, sentence):
        """Substitute correct words for placeholders for given sentence.

        Won't substitute member tag
        """
        for placeholder in re.findall(r'@\w+', sentence):
            if placeholder[1:] in self.vocab:
                sentence = sentence.replace(
                    placeholder, random.choice(self.vocab[placeholder[1:]]), 1)
        return sentence

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

    def post_meme(self, original=False):
        """
        Post Meme.

        Input:
            None
        Return:
            Message: Empty string and list of one attachment = [<meme>]
        """
        # Determine function from which to source meme
        source_meme = self.create_meme if original else self.get_meme

        # Build message with attachments
        return Message(
            attachments=[Attachment(
                type='image',
                url=source_meme(subreddits=self.settings['subreddits'])
            )])

    def create_meme(self):
        """Create Meme."""
        # member = random.choice(self.get_members())['name'].replace(' ', '_')

        # Import Meme Data
        with open(self.path + '/meme/formats.txt', 'r') as f:
            memes = json.load(f)
        meme = random.choice(list(memes.items()))
        meme_text = list(map(
            lambda x: x.replace(' ', '_'),
            random.choice(meme[1])))
        img_url = self.make_meme(meme[0], meme_text[0], meme_text[1])
        return Message(attachments=[Attachment(type='image', url=img_url)])

    def cross_map(self):
        """Mad lib against random user."""
        return self.mad_lib(reply=False)

    @staticmethod
    def load_file(path):
        """Load txt file into array and return.

        Input:
            String: Full Path to File
        Return:
            String Array: Lines of file
        """
        with open(path, 'r') as f:
            array = f.read().splitlines()
        return array

    @staticmethod
    def decision_true(probability=0.5):
        """Return True with given probability."""
        return random.random() < probability

    @staticmethod
    def get_meme(**kwargs):
        """Return Binary Image Data of a Meme.

        Input:
            None
        Return:
            Binary Image Data of Picture
        """
        subs = kwargs.get('subreddits', 'me_irl')
        s = random.choice([x for x in subs for y in range(int(subs[x]))])
        meme_url = requests.get(
            'https://meme-api.herokuapp.com/gimme/{}'.format(s)).json()['url']
        return requests.get(meme_url)

    @staticmethod
    def make_meme(meme_format, top, bottom):
        """Return url of made meme."""
        url = 'https://memegen.link/'
        # formats = list(requests.get(
        #     url + '/api/templates').json().values())
        # meme_format = random.choice(formats).rpartition('/')[2]

        return requests.get(
            url + meme_format + '/{}/{}.jpeg'.format(top, bottom))
