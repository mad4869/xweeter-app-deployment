from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_socketio import emit
from itertools import chain

from . import routes
from ..extensions import db, socket
from ..models import Xweet, User, Rexweet, follow


@socket.on("add_to_timeline")
def add_to_timeline(user_id):
    xweet = db.session.execute(
        db.select(Xweet)
        .join(User, Xweet.user_id == User.user_id)
        .filter(User.user_id == user_id)
        .order_by(Xweet.created_at.desc())
        .limit(1)
    ).scalar_one_or_none()
    xweet_data = xweet.serialize()
    xweet_data["username"] = xweet.users.username
    xweet_data["full_name"] = xweet.users.full_name
    xweet_data["profile_pic"] = xweet.users.profile_pic

    emit("add_to_timeline", xweet_data, broadcast=True)


@routes.route("/timeline", methods=["GET"], strict_slashes=False)
def get_timeline():
    start = int(request.args.get("start", 0))
    size = int(request.args.get("size", 10))

    xweets = db.session.execute(
        db.select(Xweet)
        .join(User, Xweet.user_id == User.user_id)
        .order_by(Xweet.created_at.desc())
    ).scalars()
    data = []
    for xweet in xweets:
        xweet_data = xweet.serialize()
        xweet_data["username"] = xweet.users.username
        xweet_data["full_name"] = xweet.users.full_name
        xweet_data["profile_pic"] = xweet.users.profile_pic
        data.append(xweet_data)

    end = min(start + size, len(data))

    sliced_data = data[start:end]

    return jsonify({"success": True, "data": sliced_data}), 200


@routes.route(
    "/users/<int:user_id>/profile-timeline", methods=["GET"], strict_slashes=False
)
def get_profile_timeline(user_id):
    start = int(request.args.get("start", 0))
    size = int(request.args.get("size", 10))

    own_xweets = db.session.execute(
        db.select(Xweet)
        .join(User, Xweet.user_id == User.user_id)
        .filter(User.user_id == user_id)
        .order_by(Xweet.created_at.desc())
    ).scalars()
    own_xweets_data = []
    for own_xweet in own_xweets:
        own_xweet_data = own_xweet.serialize()
        own_xweet_data["username"] = own_xweet.users.username
        own_xweet_data["full_name"] = own_xweet.users.full_name
        own_xweet_data["profile_pic"] = own_xweet.users.profile_pic
        own_xweets_data.append(own_xweet_data)

    rexweets = db.session.execute(
        db.select(Rexweet)
        .join(Xweet, Rexweet.xweet_id == Xweet.xweet_id)
        .join(User, Xweet.user_id == User.user_id)
        .filter(Rexweet.user_id == user_id)
        .order_by(Rexweet.created_at.desc())
    ).scalars()
    rexweets_data = []
    for rexweet in rexweets:
        rexweet_data = rexweet.serialize()
        rexweet_data["body"] = rexweet.xweets.body
        rexweet_data["media"] = rexweet.xweets.media
        rexweet_data["og_user_id"] = rexweet.xweets.users.user_id
        rexweet_data["og_username"] = rexweet.xweets.users.username
        rexweet_data["og_full_name"] = rexweet.xweets.users.full_name
        rexweet_data["og_profile_pic"] = rexweet.xweets.users.profile_pic
        rexweet_data["og_created_at"] = rexweet.xweets.created_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        rexweet_data["og_updated_at"] = (
            rexweet.xweets.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if rexweet.xweets.updated_at
            else rexweet.xweets.updated_at
        )
        rexweets_data.append(rexweet_data)

    timeline = list(chain(own_xweets_data, rexweets_data))
    sorted_timeline = sorted(
        timeline, key=lambda xweet: xweet["created_at"], reverse=True
    )

    end = min(start + size, len(sorted_timeline))

    sliced_timeline = sorted_timeline[start:end]

    return jsonify({"success": True, "data": sliced_timeline}), 200


@routes.route("/users/<int:user_id>/timeline", methods=["GET"], strict_slashes=False)
def get_user_timeline(user_id):
    start = int(request.args.get("start", 0))
    size = int(request.args.get("size", 10))

    own_xweets = db.session.execute(
        db.select(Xweet)
        .join(User, Xweet.user_id == User.user_id)
        .filter(User.user_id == user_id)
        .order_by(Xweet.created_at.desc())
    ).scalars()
    own_xweets_data = []
    for own_xweet in own_xweets:
        own_xweet_data = own_xweet.serialize()
        own_xweet_data["username"] = own_xweet.users.username
        own_xweet_data["full_name"] = own_xweet.users.full_name
        own_xweet_data["profile_pic"] = own_xweet.users.profile_pic
        own_xweets_data.append(own_xweet_data)

    following_xweets = db.session.execute(
        db.select(Xweet)
        .join(User, Xweet.user_id == User.user_id)
        .join(follow, User.user_id == follow.c.followed_id)
        .filter(follow.c.follower_id == user_id)
        .order_by(Xweet.created_at.desc())
    ).scalars()
    following_xweets_data = []
    for following_xweet in following_xweets:
        following_xweet_data = following_xweet.serialize()
        following_xweet_data["username"] = following_xweet.users.username
        following_xweet_data["full_name"] = following_xweet.users.full_name
        following_xweet_data["profile_pic"] = following_xweet.users.profile_pic
        following_xweets_data.append(following_xweet_data)

    timeline = list(chain(own_xweets_data, following_xweets_data))
    sorted_timeline = sorted(
        timeline, key=lambda xweet: xweet["created_at"], reverse=True
    )

    end = min(start + size, len(sorted_timeline))

    sliced_timeline = sorted_timeline[start:end]

    return jsonify({"success": True, "data": sliced_timeline}), 200
