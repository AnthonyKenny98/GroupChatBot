"""App.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 15:25:47
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-09 18:31:54

from src.groupme.groupme import GroupMeBot

from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/')
def index():
    """Basic Respond."""
    return jsonify({"Message": "Response"})


@app.route('/groupme/<randomint>', methods=['POST'])
def call_bot(randomint):
    """Call Bot."""
    bot = GroupMeBot('4a8cf510b7541a8a3c96eb17a5')
    bot.post_message("Received")
    return jsonify({"Message": "Response"})

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
