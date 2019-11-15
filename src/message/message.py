"""Message."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-11 18:14:05
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-14 18:59:27


class Message:
    """Provide class for Message."""

    def __init__(self, text='', sender=None, attachments=[]):
        """Initialize Message instance."""
        self.text = text
        self.sender = sender
        self.attachments = attachments


class Attachment:
    """Provide class for Attachment."""

    def __init__(self, type, url):
        """Initialize Attachment Instance."""
        self.type = type
        self.url = url
