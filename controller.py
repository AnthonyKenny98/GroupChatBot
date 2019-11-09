"""Main Controller Logic."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 18:40:52
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-09 18:55:31


from src.groupme.groupme import GroupMeBot


def handle(data):
    """Handle incoming data from GroupMe."""
    # Don't reply to self
    if data['user_type'] == 'bot':
        return

    # Init Bot
    bot = GroupMeBot('4a8cf510b7541a8a3c96eb17a5')

    # Post Message from Bot
    bot.post_message(str(data['text']))
