"""Main Controller Logic."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 18:40:52
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-11 12:32:01


from src.groupme.groupme import GroupMeChatBot


def groupme(data):
    """Handle incoming data from GroupMe."""
    # Wake Up Bot
    g = GroupMeChatBot(data)
    g.bot.post_message("How my dicc feel in yo ass pussy boi")
