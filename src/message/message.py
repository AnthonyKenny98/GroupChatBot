"""Message."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-11 18:14:05
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-11 18:25:50


class Message:
    """Provide class for Message."""

    def __init__(self, text=None, sender=None):
        """Initialize Message instance."""
        self.text = text
        self.sender = sender
