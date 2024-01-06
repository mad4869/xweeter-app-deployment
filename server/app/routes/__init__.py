from flask import Blueprint

routes = Blueprint("routes", __name__)

from . import auth, users, xweets, follows, rexweets, timeline, likes, replies, hashtags
