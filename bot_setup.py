"""Setup."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 17:45:01
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-15 11:36:29

from src.groupme.groupme import setup_bot
import sys

appName = input("Please enter your Heroku App Name: ")
configFile = input("Please enter your config file name \
    (without '.config' suffix")
callback_url = 'https://' + appName + '.herokuapp.com/groupme/' \
    + configFile
if sys.argv[1] == 'GroupMe':
    setup_bot(callback_url)
