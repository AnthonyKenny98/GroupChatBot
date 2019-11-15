"""Class for interfacing with GroupMe API."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 11:47:53
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-15 10:01:54

import os
import requests
import json
from ..chatbot import ChatBot
from ..message import Message

CREDENTIALS = ['GroupMeAccessToken']


class GroupMeChatBot(ChatBot):
    """Provide ChatBot Class for GroupMe.

    Inherits ChatBot class as parent class
    """

    def __init__(self, data):
        """Initialize GroupMe Chat Bot Instance.

        Input:
            -data: data posted to bot from GroupMe Webhook
        Return:
            None
        """
        # Init Parent Class
        super().__init__()

        # Init GroupMeUser instance
        self.user = GroupMe(self.get_credentials()['GroupMeAccessToken'])
        self.user.group_id = data['group_id']

        # Init GroupMeBot instance
        bots = [b for b in self.user.get_bots()
                if b['group_id'] == data['group_id']]
        self.bot = GroupMeBot(bots[0]['bot_id'])

        # Init GroupMeChatBot Name
        self.name = bots[0]['name']

        # Message that awoke the bot
        self.stimulus = Message(text=data['text'], sender=data['name'])

    def post_message(self, message):
        """Post message.

        Input:
            - message: Message instance
        Return
            - response: from self.bot.post_message
        """
        # UNCOMMENT FOR PRODUCTION
        return self.bot.post_message(
            text=message.text,
            attachments=message.attachments)

        # PRINT FOR TESTING
        # print(text)

    def pre_react_checks(self):
        """Go through API specific pre-react checks.

        Input:
            None
        Return:
            - Bool: True if proceed, False if stop
        """
        return self.stimulus.sender != self.name

    def tag_member(self):
        """Return string that for given API tags groupmember."""
        return "@" + self.stimulus.sender

    @staticmethod
    def get_credentials():
        """Return dict of credentials from either secure or example folder.

        To change credentials update the CREDENTIALS constant at the top
        of this file.
        """
        credentials = {}
        # Get credentials filepath
        path = os.path.dirname(os.path.realpath(__file__))
        if os.path.isdir(path + '/secure'):
            path += '/secure'
            for credential in CREDENTIALS:
                with open(path + '/' + credential + '.credentials', 'r') as f:
                    credentials[credential] = f.read()
        else:
            for credential in CREDENTIALS:
                credentials[credential] = os.environ[credential]
        return credentials


class GroupMe:
    """Class for interfacing with GroupMe API."""

    def __init__(self, access_token):
        """Initialize GroupMe Class Instance."""
        self.access_token = access_token
        self.authString = '?token=' + access_token
        self.baseURL = 'https://api.groupme.com/v3'
        self.headers = {'content-type': 'application/json'}
        self.group_id = None

    def build_url(self, endpoint, **kwargs):
        """Return URL for given endpoint."""
        url_path = {
            'groups': '/groups',
            'messages': '/groups/' + self.group_id + '/messages',
            'bots': '/bots',
            'members': '/groups/' + self.group_id
        }
        return self.baseURL + url_path[endpoint] + self.authString

    def get_groups(self):
        """Return JSON of groups."""
        return (requests.get(self.build_url('groups'))).json()['response']

    def get_bots(self):
        """Return list of bots."""
        return requests.get(self.build_url('bots')).json()['response']

    def get_members(self, name=None):
        """Return a list of members."""
        members = requests.get(
            self.build_url('members')).json()['response']['members']
        return members if name is None else \
            next((m for m in members if m['name'] == name), members)

    def upload_photo(self, img_data):
        """Post photo to GroupMe Image Service.

        Takes binary image data as input

        Return url for img
        """
        return requests.post(
            'https://image.groupme.com/pictures',
            headers={
                'X-Access-Token': self.access_token
            },
            data=img_data).json()['payload']['url']


class GroupMeBot:
    """Interface for GroupMe Bot."""

    def __init__(self, bot_id):
        """Initialize GroupMe Bot."""
        self.id = bot_id
        self.baseURL = 'https://api.groupme.com/v3/bots'
        self.headers = {'content-type': 'application/json'}

    def build_url(self, endpoint):
        """Return URL for given endpoint."""
        url_path = {
            'post': '/post'
        }
        return self.baseURL + url_path[endpoint]

    def post_message(self, text, attachments):
        """Send message as bot."""
        attachments = [{'type': a.type, 'url': a.url} for a in attachments]
        return requests.post(
            self.build_url('post'),
            headers=self.headers,
            data=json.dumps({
                "bot_id": self.id,
                "text": text,
                'attachments': attachments
            })
        )


def setup_bot(callback_url):
    """Set Up Bot in a particular GroupMe group chat. Return Bot ID."""
    access_token = input("Please input your GroupMe Account Access Token: ")

    groupme = GroupMe(access_token)

    # Get list of groups
    groups = groupme.get_groups()

    bot_name = input("What would you like your bot to be named: ")

    # Seek user input on group for which bot should be created
    for i in range(len(groups)):
        print(str(i) + ": " + groups[i]['name'])
    group_index = int(input("\nInput Group Number For Bot: "))

    # Prepare payload to create bot
    payload = json.dumps({
        "bot": {
            "name": bot_name,
            "group_id": groups[group_index]['id'],
            "callback_url": callback_url
        }
    })
    url = groupme.build_url('bots')

    # Make Post request
    response = requests.post(url, headers=groupme.headers, data=payload)
    print('Success' if response.status_code == 201 else 'Failure')
