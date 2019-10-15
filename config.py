"""Config vars"""
import os
from apiclient.discovery import build

PRAW_SECRET = os.environ.get('PRAW_SECRET', None)
PRAW_KEY = os.environ.get('PRAW_KEY', None)
PRAW_USER_AGENT = os.environ.get('PRAW_USER_AGENT', None)
#  These CSV locations will differ for you
ARTICLES_CSV_LOCATION = "s3://wsankey-capstone/articlecsvs/"
COMMENTS_CSV_LOCATION = "s3://wsankey-capstone/commentcsvs/"
YOUTUBE_CSV_LOCATION = "s3://wsankey-capstone/youtubecsvs/"

CLUSTER = 'redshift-cluster-1'
USER = os.environ.get('AWSUSER', None)
PASSWORD = os.environ.get('AWSUSER_PW', None)
DBNAME = 'dev'
PORT = 5439
HOST = os.environ.get('REDSHIFT_HOST', None)
ARN = os.environ.get('REDSHIFT_ARN', None)


DEVELOPER_KEY = os.environ["DEVELOPER_KEY"]
URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


#  Subreddits the lambda chooses amongst
SUBREDDITS = [
    "gaming",
    "gamedev",
    "indiegames",
    "devblogs",
    "gamedesign",
    "ludology",
    "gamesociety",
    "gamernews",
    "truegaming",
    "leagueoflegends",
    "overwatch",
    "pokemon",
    "pokemongo",
    "fortnitebr",
    "hearthstone",
    "wow",
    "minecraft",
    "destinythegame",
    "globaloffensive",
    "skyrim",
    "zelda",
    "fallout",
    "dota2",
    "rokeyleague",
    "kerbalspaceprogram",
    "reddeadredemption",
    "totalwar",
    "stardewvalley",
    "civ",
    "smashbros",
    "eve"
    "terraria",
    "blender",
    "design",
    "photoshopbattles",
    "graphic_design",
    "logodesign"
]
