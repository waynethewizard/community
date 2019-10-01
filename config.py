"""Config vars"""
import os
PRAW_SECRET = os.environ.get('PRAW_SECRET', None)
PRAW_KEY = os.environ.get('PRAW_KEY', None)
PRAW_USER_AGENT = os.environ.get('PRAW_USER_AGENT', None)