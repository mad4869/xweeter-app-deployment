from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import routes
from ..extensions import db
from ..models import Xweet, User, Rexweet


@routes.route(
    "/xweets/<int:xweet_id>/rexweets",
    methods=["GET"],
    strict_slashes=False,
)
def get_rexweets_by_xweet(xweet_id):
    rexweets = db.session.execute(
        db.select(Rexweet)
        .join(Xweet, Rexweet.xweet_id == Xweet.xweet_id)
        .join(User, Xweet.user_id == User.user_id)
        .filter(Rexweet.xweet_id == xweet_id)
        .order_by(Rexweet.created_at.desc())
    ).scalars()
    data = []
    for rexweet in rexweets:
        serial = rexweet.serialize()
        serial.update(
            {
                "body": rexweet.xweets.body,
                "media": rexweet.xweets.media,
                "og_user_id": rexweet.xweets.users.user_id,
                "og_username": rexweet.xweets.users.username,
                "og_full_name": rexweet.xweets.users.full_name,
                "og_profile_pic": rexweet.xweets.users.profile_pic,
            }
        )
        data.append(serial)

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/<int:user_id>/rexweets", methods=["GET"], strict_slashes=False)
def get_rexweets_by_user(user_id):
    rexweets = db.session.execute(
        db.select(Rexweet)
        .join(Xweet, Rexweet.xweet_id == Xweet.xweet_id)
        .join(User, Xweet.user_id == User.user_id)
        .filter(Rexweet.user_id == user_id)
        .order_by(Rexweet.created_at.desc())
    ).scalars()
    data = []
    for rexweet in rexweets:
        serial = rexweet.serialize()
        serial.update(
            {
                "body": rexweet.xweets.body,
                "media": rexweet.xweets.media,
                "og_user_id": rexweet.xweets.users.user_id,
                "og_username": rexweet.xweets.users.username,
                "og_full_name": rexweet.xweets.users.full_name,
                "og_profile_pic": rexweet.xweets.users.profile_pic,
            }
        )
        data.append(serial)

    return jsonify({"success": True, "data": data}), 200


@routes.route(
    "/users/<int:user_id>/xweets/<int:xweet_id>/rexweets",
    methods=["POST", "DELETE"],
    strict_slashes=False,
)
@jwt_required()
def access_rexweets_by_user_xweet(user_id, xweet_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"success": False, "message": "Unauthorized action"}), 403

    if request.method == "POST":
        rexweet = Rexweet(user_id=user_id, xweet_id=xweet_id)

        try:
            db.session.add(rexweet)
            db.session.commit()
        except:
            db.session.rollback()

            return (
                jsonify({"success": False, "message": "Failed to rexweet"}),
                500,
            )
        else:
            return jsonify({"success": True, "data": rexweet.serialize()}), 201

    elif request.method == "DELETE":
        rexweet = db.session.execute(
            db.select(Rexweet).filter(
                Rexweet.xweet_id == xweet_id, Rexweet.user_id == user_id
            )
        ).scalar_one_or_none()

        try:
            db.session.delete(rexweet)
            db.session.commit()
        except:
            db.session.rollback()

            return (
                jsonify({"success": False, "message": "Failed to unrexweet"}),
                500,
            )
        else:
            return (
                jsonify({"success": True, "data": rexweet.serialize()}),
                201,
            )
