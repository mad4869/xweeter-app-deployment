from .hashtag_xweet import hashtag_xweet
from .. import db


class Hashtag(db.Model):
    __tablename__ = "hashtags"
    hashtag_id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.String(140), nullable=False, unique=True)
    xweets = db.Relationship(
        "Xweet",
        secondary=hashtag_xweet,
        backref=db.backref("hashtags", lazy="dynamic"),
        lazy="dynamic",
    )

    def serialize(self):
        return {
            "hashtag_id": self.hashtag_id,
            "body": self.body,
        }

    def __repr__(self):
        return f"{self.body}"
