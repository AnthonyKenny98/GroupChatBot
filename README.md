<img src="img/mrchatterbox.png" alt="project logo image" width="100"/>

# Group Chat Bot &middot; [![Known Vulnerabilities](https://snyk.io/test/github/AnthonyKenny98/GroupChatBot/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/AnthonyKenny98/GroupChatBot?targetFile=requirements.txt) [![Build Status](https://travis-ci.org/AnthonyKenny98/GroupChatBot.svg?branch=master)](https://travis-ci.org/AnthonyKenny98/GroupChatBot) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/AnthonyKenny98/Vend_Inventory_Upload/blob/master/LICENSE)
> Anthony Kenny.

Currently supports:
  - GroupMe
  
## Table of Contents

+ [Prerequisites](#prereq)
+ [Installation/Setup](#setup): Instructions for setting up your own chatbot.
+ [API Reference](#api)
+ [Licensing](#license)


## <a name="prereq"></a>Prerequisites
+ [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli): to setup a server for hosting your bots.
+ [Travis Account](https://travis-ci.org/): Optional, for CI if you fork this repo.
+ [Python 3.7.5](https://www.python.org/downloads/release/python-275/)
+ [GroupMe Developer Account](https://dev.groupme.com/): This is the same as your GroupMe Account. Your Access Token can be found here.

## <a name="setup"></a>Installation/Setup

### Checkout the Code 
  ```
  $ git clone https://github.com/AnthonyKenny98/GroupChatBot.git
  $ cd GroupChatBot
  ```
### Create and Init Virtual Environment
  ```
  $ virtualenv venv
  $ source venv/bin/activate
  ```
### Install Dependencies
  ```
  $ pip3 install -r requirements.txt
  ```
### Setup Heroku (You will need your Heroku Account Credentials).
You will be prompted to enter a Heroku App Name. Name must start with a letter, end with a letter or digit and can only contain lowercase letters, digits, and dashes.
The script will push the application to the heroku server and install all neccesary dependencies.
  ```
  $ ./scripts/heroku_setup.sh
  ```
### Setup a Bot
The following can be repeated for as many bots in as many groupchats as you would like. You will be prompted for your GroupMe Access Token.
  ```
  $ ./scripts/bot_setup.sh
  ```
Congratulations, you have set up your first bot!

## <a name="api"></a>Api Reference

[GroupMe API](https://dev.groupme.com/).

[Meme API](https://github.com/R3l3ntl3ss/Meme_Api)

## <a name="license"></a>Licensing

This project is licensed under the MIT License.  See the [LICENSE](LICENSE) file for more information.
