#!/usr/bin/python
import datetime as dt
import json
import logging
import requests
import pprint
from collections import namedtuple

import pandas as pd
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from config import YOUTUBE

Response = namedtuple('Response', ['stats', 'snippet', 'channel'])


def ysearch(term, maxn=50, date=None):
    """
    Args:
        term (str): Search term
        maxn (int): Number of results to return

    Returns:
        list of dictionaries
    """
    response = YOUTUBE.search().list(q=term, part="id,snippet",
                                     maxResults=maxn).execute()
    return response


def yvideos(response):
    """
    Args:
        response (dict)

    Returns:
        list
    """
    ids = []
    items = response.get("items", [])

    for result in items:
        if result["id"]["kind"] == "youtube#video":
            ids.append(result["id"]["videoId"])
        else:
          print("Not a video, instead it's a", result["id"]["kind"])

    return ids


def video_information(result):
    """
    Args:
        result (namedtuple)
        'stats', 'snippet'

    Returns:
        dictionary
    """
    info = None

    snippet = result.snippet['items'][0]['snippet']
    stats = result.stats['items'][0]['statistics']
    channel = result.channel['items'][0]['statistics']

    now_iso = dt.datetime.utcnow().isoformat()
    now_str = str(now_iso)

    try:
        video_id = result.stats['items'][0]['id']
        unique_id = video_id + now_str
        desc = snippet['description']
        if desc == '':
            desc = 'No description'

        info = dict(#_id=unique_id,
                    #video_id=video_id,
                    title=snippet['title'].encode(encoding='UTF-8', errors='replace'),
                    #description=desc,
                    #thumbnail=snippet['thumbnails']['high']['url'],
                    channel_title=snippet['channelTitle'].encode(encoding='UTF-8', errors='replace'),
                    channel_id=snippet['channelId'].encode(encoding='UTF-8', errors='replace'),
                    #category_id=snippet['categoryId'],
                    #tags=snippet['tags'],
                    #published_at=snippet['publishedAt'],
                    comment_count=int(stats.get('commentCount', 0)),
                    #dislike_count=stats.get('dislikeCount', 0),
                    #favorite_count=stats.get('favoriteCount', 0),
                    like_count=int(stats.get('likeCount', 0)),
                    view_count=int(stats.get('viewCount', 0)),
                    #accessed_at=now_iso,
                    #channel_comment_count=channel.get('commentCount', 0),
                    #channel_hidden_subscriber_count=channel.get('hiddenSubscriberCount', False),
                    #channel_subscriber_count=channel.get('subscriberCount', 0),
                    #channel_video_count=channel.get('videoCount', 0),
                    #channel_view_count=channel.get('viewCount', 0)
                    )
    except KeyError:
        logging.info('Failed to format item from YouTube', result)

    return info


def video_stats(video_id):
    """
    Args:
        videos (dictionary)

    Returns:
        dictionary

    """
    stats = YOUTUBE.videos().list(
    id=video_id,
    part="statistics",
    ).execute()

    snippet = YOUTUBE.videos().list(
    id=video_id,
    part="snippet",
    ).execute()

    # Channel information
    channel = YOUTUBE.channels().list(
    id=snippet['items'][0]['snippet']['channelId'],
    part="statistics",
    ).execute()

    data = Response(stats, snippet, channel)
    return data


if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term")
  argparser.add_argument("--maxn", help="Max results", default=25)
  args = argparser.parse_args()

  try:
    response = ysearch(args.q, args.maxn, date=None)
    videos = yvideos(response)
    all_data = []
    for video_id in videos:
        data = video_stats(video_id)
        info = video_information(data)
        #pprint.pprint(info)
        if info is not None:
            all_data.append(info)
    pprint.pprint(all_data[0])
    df = pd.DataFrame(all_data)
    pprint.pprint(df.head())
    df.to_csv(args.q + '.csv')
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
