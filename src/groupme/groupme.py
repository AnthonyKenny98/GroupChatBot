"""Class for interfacing with GroupMe API."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 11:47:53
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-11 12:28:51

import requests
import json

ACCESS_TOKEN = 'NCSnlZKP4kcnnkQXZd7SBql045OHQrOXYgHyYiim'
TEST_GROUP_ID = '55604032'


class GroupMeChatBot:
    """Master ChatBot Class for GroupMe."""

    def __init__(self, message):
        """Initialize GroupMe Chat Bot Instance."""
        # Message that awoke the bot
        self.message = message

        # Init GroupMeUser instance
        self.user = GroupMe(ACCESS_TOKEN)

        # Get correct bot for callback_data
        self.bot = GroupMe([
            b for b in self.user.get_bots()
            if b['group_id'] == self.message['group_id']
        ][0]['bot_id'])

        self.react()

    def react(self):
        """React to the message that awoke the bot."""
        # Do not react to own message
        if self.message['sender_id'] == self.bot.id:
            return
        else:
            self.bot.post_message("How my dick feel in yo ass pussy boi")


class GroupMe:
    """Class for interfacing with GroupMe API."""

    def __init__(self, access_token):
        """Initialize GroupMe Class Instance."""
        self.authString = '?token=' + access_token
        self.baseURL = 'https://api.groupme.com/v3'
        self.headers = {'content-type': 'application/json'}

    def build_url(self, endpoint, **kwargs):
        """Return URL for given endpoint."""
        url_path = {
            'groups': '/groups',
            'messages': '/groups/' + kwargs.get('groupID', '') + '/messages',
            'bots': '/bots'
        }
        return self.baseURL + url_path[endpoint] + self.authString

    def get_groups(self):
        """Return JSON of groups."""
        return (requests.get(self.build_url('groups'))).json()['response']

    def get_bots(self):
        """Return list of bots."""
        return requests.get(self.build_url('bots')).json()['response']


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
            'post': '/bots/post'
        }
        return self.baseURL + url_path[endpoint]

    def post_message(self, text):
        """Send message as bot."""
        return requests.post(
            self.build_url('post'),
            headers=self.headers,
            data=json.dumps({
                "bot_id": self.id,
                "text": text
            })
        )


def setup_bot(callback_url):
    """Set Up Bot in a particular GroupMe group chat. Return Bot ID."""
    groupme = GroupMe(ACCESS_TOKEN)

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
