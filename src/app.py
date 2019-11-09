"""App.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 15:25:47
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-09 17:17:17

from flask import Flask, jsonify  # , request
app = Flask(__name__)


@app.route('/')
def index():
    """Basic Respond."""
    return jsonify({"Message": "Response"})


@app.route('/callbot/<bot_id>')
def call_bot(bot_id):
    """Call Bot."""
    return jsonify({"ID": bot_id})

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
