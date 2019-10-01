"""
Grab data, start with Reddit, as json blobs and store them in S3.
1. Connect to reddit
2. Grab json data
3. Store json in S3
"""
import datetime as dt
import praw
from praw.models import MoreComments

import boto3
import json

from config import PRAW_SECRET, PRAW_KEY, PRAW_USER_AGENT


def reddit_instance():
  """
  Return instance of reddit
  """
  reddit = praw.Reddit(client_id=PRAW_KEY,
                       client_secret=PRAW_SECRET,
                       user_agent=PRAW_USER_AGENT)
  return reddit


def clean_submission(submission):
    """
    Take Reddit submission and turn into dictionary
    """
    now_iso = dt.datetime.utcnow().isoformat()
    created_iso = dt.datetime.utcfromtimestamp(submission.created_utc).isoformat()
    try:
        submission_author = submission.author.name
    except:
        submission_author = "None"
    data = {
        "id": submission.id,
        "title": submission.title,
        "score": submission.score,
        "url": submission.url,
        "name": submission.name,
        "author": submission_author,
        "is_video": submission.is_video,
        "over_18": submission.over_18,
        "selftext": submission.selftext,
        "shortlink": submission.shortlink,
        "subreddit_type": submission.subreddit_type,
        "subreddit_subscribers": submission.subreddit_subscribers,
        "thumbnail": submission.thumbnail,
        "ups": submission.ups,
        "created_utc": created_iso,
        "archived": now_iso
    }
    for k, v in data.items():
        if v == "":
            data[k] = "None"
    return data

def clean_comment(comment):
    """
    Clean the comment
    """
    try:
        name = comment.author.name
    except:
        name = "None"
    data = {
        "author": name,
        "body": comment.body,
        "ups": comment.ups,
        "fullname": comment.fullname
    }
    for k, v in data.items():
        if v == "":
            data[k] = "None"
    return data


def subreddit_type_submissions(sub="writing", kind="hot"):
    """
    Connects to subreddit (sub) then
    iterates through submissions and returns them
    in list.
    """
    comments = []
    articles = []
    red = reddit_instance()
    subreddit = red.subreddit(sub)
    if kind == "hot":
        submissions = subreddit.hot()
    elif kind == "top":
        submissions = subreddit.top()
    elif kind == "new":
        submissions = subreddit.new()
    elif kind == "random_rising":
        submissions = subreddit.random_rising()
    else:
        assert False

    for submission in submissions:
        article = clean_submission(submission)
        article['subreddit'] = sub
        articles.append(article)

        for top_level_comment in submission.comments:
            # if isinstance(top_level_comment, MoreComments):
            #     continue
            comment = clean_comment(top_level_comment)
            comment['article_id'] = article['id']
            comments.append(comment)

    return articles, comments


def data_for_subreddit(sub, kind="new"):
    """
    """
    #for kind in themes:
    print("Pulling posts from {}, {}".format(sub, kind))
    articles, comments = subreddit_type_submissions(sub, kind)
    return articles, comments


if __name__ == "__main__":
    assert PRAW_KEY is not None
    articles, comments = data_for_subreddit("gaming")
    print(comments)