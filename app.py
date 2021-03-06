"""App.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 15:25:47
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2020-03-23 19:09:48

from src.groupme import GroupMeChatBot
from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/')
def index():
    """Basic Respond."""
    return jsonify({"Message": "Response"})


@app.route('/groupme/<config>/<randint>', methods=['POST'])
def call_bot(config, randint):
    """Call Bot."""
    GroupMeChatBot(request.json, config=config).react()
    return jsonify({"Message": "Response"})


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
