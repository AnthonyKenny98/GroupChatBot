"""Reddit."""

# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-16 18:35:52
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-17 14:22:36

import praw
import os

USER_AGENT = 'GroupMeChatBot'
CREDENTIALS = ['RedditClientID', 'RedditClientSecret']


class Reddit:
    """Provide Client Info."""

    def __init__(self):
        """Init."""
        creds = self.get_credentials()
        self.reddit = praw.Reddit(
            client_id=creds['RedditClientID'],
            client_secret=creds['RedditClientSecret'],
            user_agent=USER_AGENT)

    def get_submissions(self, subreddit, method='rand', limit=100):
        """Get submissions from a given subreddit."""
        method_selector = {
            'hot': self.reddit.subreddit(subreddit).hot,
            'top': self.reddit.subreddit(subreddit).top,
            'new': self.reddit.subreddit(subreddit).new
        }
        return [self.reddit.subreddit(subreddit).random()] if method == 'rand'\
            else list(method_selector[method](limit=limit))

    def get_comments(self, post):
        """Get comments."""
        post.comments.replace_more(limit=1)
        return post.comments

    @staticmethod
    def is_img_url(url):
        """Check if url is an image."""
        return url[-4:] == '.jpg' or url[-4:] == '.png'

    @staticmethod
    def get_credentials():
        """Return dict of credentials from either secure folder or environ variables.

        To change credentials update the CREDENTIALS constant at the top
        of this file.
        """
        credentials = {}
        # Get credentials filepath
        path = os.path.dirname(os.path.realpath(__file__))
        if os.path.isdir(path + '/secure'):
            path += '/secure'
            for credential in CREDENTIALS:
                with open(path + '/' + credential + '.credentials', 'r') as f:
                    credentials[credential] = f.read()
        else:
            for credential in CREDENTIALS:
                credentials[credential] = os.environ[credential]
        return credentials
