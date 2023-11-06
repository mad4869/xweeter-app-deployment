from flask import Blueprint
import logging

routes = Blueprint("routes", __name__)

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

from . import auth, users, xweets, follows, rexweets, timeline, likes, replies, hashtags
