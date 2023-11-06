from datetime import datetime

from .. import db


class Rexweet(db.Model):
    __tablename__ = "rexweets"
    rexweet_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.user_id"))
    xweet_id = db.Column(db.Integer(), db.ForeignKey("xweets.xweet_id"))
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime())

    def serialize(self):
        return {
            "rexweet_id": self.rexweet_id,
            "user_id": self.user_id,
            "xweet_id": self.xweet_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.updated_at
            else self.updated_at,
        }

    def __repr__(self):
        return f"{self.user_id} rexweets {self.xweet_id}"
