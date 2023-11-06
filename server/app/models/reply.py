from datetime import datetime

from .. import db


class Reply(db.Model):
    __tablename__ = "replies"
    reply_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.user_id"))
    xweet_id = db.Column(db.Integer(), db.ForeignKey("xweets.xweet_id"))
    body = db.Column(db.String(140), nullable=False)
    media = db.Column(db.Text())
    media_name = db.Column(db.Text())
    media_updated_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime())

    def serialize(self):
        return {
            "reply_id": self.reply_id,
            "user_id": self.user_id,
            "xweet_id": self.xweet_id,
            "body": self.body,
            "media": self.media,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.updated_at
            else self.updated_at,
        }

    def __repr__(self):
        return f"{self.body}"
