"""
Grab data, start with Reddit, as json blobs and store them in S3.
1. Connect to reddit
2. Grab json data
3. Store json in S3
"""
import datetime as dt
import praw
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


def clean_submission(article_id, submission):
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
        article_id : {
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
    }
    for k, v in data[submission.id].items():
        if v == "":
            data[k] = "None"
    return data

def clean_comment(_id, comment):
    """
    Clean the comment
    """
    now_iso = dt.datetime.utcnow().isoformat()
    created_iso = dt.datetime.utcfromtimestamp(comment.created_utc).isoformat()
    try:
        name = comment.author.name
    except:
        name = "None"
    data = {
        _id : {
            "author": name,
            "body": comment.body,
            "ups": comment.ups,
            "fullname": comment.fullname,
            "created_utc": created_iso,
            "subreddit": str(comment.subreddit)
        }
    }
    for k, v in data[hash(comment.body)].items():
        if v == "":
            data[k] = "None"
    return data


def subreddit_type_submissions(submissions):
    """
    Connects to subreddit (sub) then
    iterates through submissions and returns them
    in list.
    """
    comments = {}
    articles = {}

    for submission in submissions:
        article_id = submission.id
        article = clean_submission(article_id, submission)
        article[article_id]['subreddit'] = str(submission.subreddit)
        articles.update(article)

        submission.comments.replace_more(limit=0)
        for top_level_comment in submission.comments:
            _id = hash(top_level_comment.body)
            comment = clean_comment(_id, top_level_comment)
            comment[hash(top_level_comment.body)]['article_id'] = article_id
            comments.update(comment)

    return articles, comments


def data_for_subreddit(submissions):
    """
    """
    articles, comments = subreddit_type_submissions(submissions)
    return articles, comments


def save_articles_and_comments(sub, submissions):
    """
    """
    s3 = boto3.resource('s3')
    now = dt.datetime.utcnow()
    formatted_date = now.strftime("%Y-%m-%d-%H-%M-%S")

    articles, comments = data_for_subreddit(submissions)
    print("Number of articles, comments {}, {}".format(len(articles), len(comments)))
    articles_name = 'articles/' + formatted_date + '_' + sub + '_articles.json'
    comments_name = 'comments/' + formatted_date + '_' + sub + '_comments.json'
    object = s3.Object('wsankey-capstone', articles_name)
    object.put(Body=json.dumps(articles))
    print("Finished writing articles to {}".format(articles_name))

    object = s3.Object('wsankey-capstone', comments_name)
    object.put(Body=json.dumps(comments))
    print("Finished writing comments to {}".format(comments_name))


if __name__ == "__main__":
    assert PRAW_KEY is not None
    sub = "gaming"
    red = reddit_instance()
    subreddit = red.subreddit(sub)

    print("Pulling posts from {}, {}.".format(sub, "hot"))
    submissions = subreddit.hot()
    save_articles_and_comments(sub, submissions)
    print("="*50)

    print("Pulling posts from {}, {}.".format(sub, "new"))
    submissions = subreddit.new()
    save_articles_and_comments(sub, submissions)
    print("="*50)

    print("Pulling posts from {}, {}.".format(sub, "top"))
    submissions = subreddit.top()
    save_articles_and_comments(sub, submissions)
    print("="*50)

    print("Pulling posts from {}, {}.".format(sub, "rising"))
    submissions = subreddit.rising()
    save_articles_and_comments(sub, submissions)
