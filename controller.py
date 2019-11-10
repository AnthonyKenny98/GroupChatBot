"""Main Controller Logic."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 18:40:52
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-10 08:44:17


from src.groupme.groupme import GroupMeBot, GroupMe


def handle(data):
    """Handle incoming data from GroupMe."""
    # Don't reply to self
    if data['sender_type'] == 'bot':
        return

    groupme = GroupMe('NCSnlZKP4kcnnkQXZd7SBql045OHQrOXYgHyYiim')

    # Get list of bots
    bots = groupme.get_bots()

    bot_id = None
    for bot in bots:
        if bot['group_id'] == data['group_id']:
            bot_id = bot['bot_id']

    if bot_id is None:
        return

    # Init Bot
    bot = GroupMeBot(bot_id)

    # Post Message from Bot
    bot.post_message("I'm Back Bitch")
