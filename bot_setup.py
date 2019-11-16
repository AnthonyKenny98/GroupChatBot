"""Setup."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 17:45:01
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-16 14:57:07

from src.groupme.groupme import setup_bot
import random

options = {
    "0": "GroupMe"
}

# Get Heroku App Name
appName = input("Please enter your Heroku App Name: ")

# Get Config Filename
configFile = input(
    "Please enter your configuration filename (without '.config' suffix): ")

print("\n\nApplications\n==========")
for key, val in options.items():
    print(key + ' : ' + val)
print("\n")

service = None
while (service not in options):
    service = input("Please input your Application option number: ")
service = options[service]

# Construct CallBack URL
callback_url = 'https://{}.herokuapp.com/{}/{}/{}'.format(
    appName,
    service.lower(),
    configFile,
    str(random.randint(0, 1000000)))

if service == 'GroupMe':
    setup_bot(callback_url)
