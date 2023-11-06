from datetime import datetime

from .. import db

hashtag_xweet = db.Table(
    "hashtags_xweets",
    db.Column(
        "xweet_id", db.Integer(), db.ForeignKey("xweets.xweet_id"), primary_key=True
    ),
    db.Column(
        "hashtag_id",
        db.Integer(),
        db.ForeignKey("hashtags.hashtag_id"),
        primary_key=True,
    ),
    db.Column("created_at", db.DateTime(), nullable=False, default=datetime.now),
)
