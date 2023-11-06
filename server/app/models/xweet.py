from datetime import datetime

from .hashtag_xweet import hashtag_xweet
from .. import db


class Xweet(db.Model):
    __tablename__ = "xweets"
    xweet_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.user_id"))
    body = db.Column(db.String(140))
    media = db.Column(db.Text())
    media_name = db.Column(db.Text())
    media_updated_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime())
    replies = db.Relationship(
        "Reply", backref="xweets", lazy=True, cascade="all, delete-orphan"
    )
    rexweets = db.Relationship(
        "Rexweet", backref="xweets", lazy=True, cascade="all, delete-orphan"
    )
    likes = db.Relationship(
        "Like", backref="xweets", lazy=True, cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "xweet_id": self.xweet_id,
            "user_id": self.user_id,
            "body": self.body,
            "media": self.media,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.updated_at
            else self.updated_at,
        }

    def __repr__(self):
        return f"{self.body}"
