"""App.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 15:25:47
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-11 23:14:11

from src.groupme import GroupMeChatBot
from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/')
def index():
    """Basic Respond."""
    return jsonify({"Message": "Response"})


@app.route('/groupme/<randomint>', methods=['POST'])
def call_bot(randomint):
    """Call Bot."""
    GroupMeChatBot(request.json).react()
    return jsonify({"Message": "Response"})


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
