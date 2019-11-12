"""Setup."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 17:45:01
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-11 19:50:37

from src.groupme.groupme import setup_bot
import random
import sys


appName = input("Please enter your Heroku App Name: ")
callback_url = 'https://' + appName + '.herokuapp.com/groupme/' \
    + str(random.randint(0, 100000))
if sys.argv[1] == 'GroupMe':
    setup_bot(callback_url)
