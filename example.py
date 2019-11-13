"""Example."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-11 14:53:27
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-13 15:08:09

from src.groupme import GroupMeChatBot


data = {
    'attachments': [],
    'avatar_url': 'https://i.groupme.com/ \
        750x750.jpeg.b5c60559b63741f39f499aec0f171cf0',
    'created_at': 1573493995,
    'group_id': '55604032',
    'id': '157349399548016936',
    'name': 'Anthony Kenny',
    'sender_id': '41327836',
    'sender_type': 'user',
    'source_guid': '5719AB7F-D7C2-4523-B665-14D6DCE91DE6',
    'system': False,
    'text': '"This is a test message"',
    'user_id': '41327836'
}

print(GroupMeChatBot(data).choose_function())
