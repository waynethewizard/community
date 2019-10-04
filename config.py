"""Config vars"""
import os
PRAW_SECRET = os.environ.get('PRAW_SECRET', None)
PRAW_KEY = os.environ.get('PRAW_KEY', None)
PRAW_USER_AGENT = os.environ.get('PRAW_USER_AGENT', None)

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
]
