from datetime import datetime

from .. import db

follow = db.Table(
    "follows",
    db.Column(
        "followed_id", db.Integer(), db.ForeignKey("users.user_id"), primary_key=True
    ),
    db.Column(
        "follower_id", db.Integer(), db.ForeignKey("users.user_id"), primary_key=True
    ),
    db.Column("created_at", db.DateTime(), nullable=False, default=datetime.now),
    db.Column("updated_at", db.DateTime()),
)
