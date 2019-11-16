"""Chatbot.py."""

# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-11 13:31:40
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-16 16:27:43

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
        """Initialize ChatBot."""
        # Import config settings
        config = 'default' if config is None else config
        self.path = os.path.dirname(os.path.realpath(__file__))
        with open(self.path + '/config/' + config + '.config', 'r') as f:
            self.settings = json.load(f)

        # Adjust settings types
        self.settings['bravery'] = float(self.settings['bravery'])

        # Empty stimulus, loaded in Child.init()
        self.stimulus = None

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
        """React to message that awoke the bot."""
        # Execute Logic to decide whether to react
        #   1) Conduct API specific pre-react checks
        if not self.pre_react_checks():
            return

        #   2) Always reply if called out
        if self.name.lower() not in self.stimulus.text.lower():
            #   3) With probability inversely proportional to bravery setting,a
            #   don't react
            if self.settings['bravery'] < random.uniform(0, 1):
                return

        # Post response
        self.post_message(self.choose_function()())

    def choose_function(self):
        """Return a class method according to probability in config file."""
        # Parse stimulus
        pdf = self.settings['random_function_call_pdf']
        if 'meme' in self.stimulus.text.lower():
            options = [self.meme]
        elif self.name.lower() in self.stimulus.text.lower():
            options = [
                self.mad_lib * pdf['mad_lib'],
                self.spongebob_mock * pdf['spongebob_mock']]
        else:
            selector = {
                'mad_lib': self.mad_lib,
                'spongebob_mock': self.spongebob_mock,
                'post_meme': self.meme,
                'cross_map': self.cross_map,
                'create_meme': self.create_meme
            }
            funcs = {}
            for key, val in self.settings['random_function_call_pdf'].items():
                funcs[selector[key]] = int(val)
            options = [x for x in funcs for y in range(funcs[x])]
        return random.choice(options)

    def introduce(self):
        """Return Message Object with introduction."""
        return Message(text='Hello, my name is {}'.format(self.name))

    def mad_lib(self, reply=True):
        """
        Create Mad Lib from self.vocab.

        Return
        ------
        Message
            text = Comleted Mad Lib
        """
        # Choose Sentence
        sentence = ''
        while sentence == '' or (not reply and '@member' not in sentence):
            sentence = random.choice(self.vocab['sentence'])

        # Replace member tag
        sentence = sentence.replace('@member', self.tag_member(reply=reply))

        # Return Message with placeholders substituted
        return Message(text=self.sub_placeholders(sentence))

    def cross_map(self):
        """Mad lib against a random user."""
        return self.mad_lib(reply=False)

    def spongebob_mock(self):
        """
        Capitalize every second letter.

        Credit: https://stackoverflow.com/a/17865821

        Return
        ------
        Message
            text = Alternating capitalized version of self.stimulus.text
        """
        cap = [True]

        def repl(m):
            cap[0] = not cap[0]
            return m.group(0).upper() if cap[0] else m.group(0).lower()
        return Message(
            text=re.sub(r'[A-Za-z]', repl, self.stimulus.text))

    def meme(self, original=False):
        """
        Create a Message with a Meme.

        Return
        ------
        Message
            attachments = [Attachment(<meme>)]
        """
        # Determine function from which to source meme
        source_meme = self.create_meme if original else self.get_meme

        # Build message with attachments
        return Message(
            attachments=[Attachment(
                type='image',
                url=source_meme(subreddits=self.settings['subreddits'])
            )])

    def sub_placeholders(self, sentence):
        """Substitute correct words for placeholders for given sentence.

        Won't substitute @member
        """
        for placeholder in re.findall(r'@\w+', sentence):
            if placeholder[1:] in self.vocab:
                sentence = sentence.replace(
                    placeholder, random.choice(self.vocab[placeholder[1:]]), 1)
        return sentence

    def create_meme(self):
        """(In Development) Create Meme."""
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

    @staticmethod
    def load_file(path):
        """Load txt file lines into array and return."""
        with open(path, 'r') as f:
            array = f.read().splitlines()
        return array

    @staticmethod
    def get_meme(**kwargs):
        """Return Binary Image Data of a Meme.

        Return
        ------
            url
        """
        subs = kwargs.get('subreddits', 'me_irl')
        s = random.choice([x for x in subs for y in range(int(subs[x]))])
        meme_url = requests.get(
            'https://meme-api.herokuapp.com/gimme/{}'.format(s)).json()['url']
        return meme_url

    @staticmethod
    def make_meme(meme_format, top, bottom):
        """Return url of made meme."""
        url = 'https://memegen.link/'
        # formats = list(requests.get(
        #     url + '/api/templates').json().values())
        # meme_format = random.choice(formats).rpartition('/')[2]

        return requests.get(
            url + meme_format + '/{}/{}.jpeg'.format(top, bottom))
