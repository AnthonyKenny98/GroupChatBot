"""Main Controller Logic."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 18:40:52
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-10 08:39:18


from src.groupme.groupme import GroupMeBot, GroupMe


def handle(data):
    """Handle incoming data from GroupMe."""
    # Don't reply to self
    if data['sender_type'] == 'bot':
        return

    groupme = GroupMe('NCSnlZKP4kcnnkQXZd7SBql045OHQrOXYgHyYiim')

    bots = [b for b in groupme.get_bots() if b['bot_id'] == data['group_id']]

    if len(bots) == 0:
        return

    # Init Bot
    bot = GroupMeBot('4a8cf510b7541a8a3c96eb17a5')

    # Post Message from Bot
    bot.post_message(bots)
