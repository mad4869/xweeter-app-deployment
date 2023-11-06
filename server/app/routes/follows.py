from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import routes, logging
from ..extensions import db, jwt_manager
from ..models import User, follow


@routes.route("/users/<int:user_id>/following", methods=["GET"], strict_slashes=False)
def get_user_following(user_id):
    followings = db.session.execute(
        db.select(User)
        .join(follow, User.user_id == follow.c.followed_id)
        .filter(follow.c.follower_id == user_id)
        .order_by(follow.c.created_at.desc())
    ).scalars()
    data = [following.serialize() for following in followings]

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/<int:user_id>/followers", methods=["GET"], strict_slashes=False)
def get_user_followers(user_id):
    followers = db.session.execute(
        db.select(User)
        .join(follow, User.user_id == follow.c.follower_id)
        .filter(follow.c.followed_id == user_id)
        .order_by(follow.c.created_at.desc())
    ).scalars()
    data = [follower.serialize() for follower in followers]

    return jsonify({"success": True, "data": data}), 200


@routes.route(
    "/users/<int:follower_id>/follows/<int:followed_id>",
    methods=["POST"],
    strict_slashes=False,
)
@jwt_required()
def follows(follower_id, followed_id):
    current_user_id = get_jwt_identity()
    if current_user_id != follower_id:
        return jsonify({"success": False, "message": "Unauthorized action"}), 403

    try:
        db.session.execute(
            follow.insert().values(followed_id=followed_id, follower_id=follower_id)
        )
        db.session.commit()
    except Exception as err:
        db.session.rollback()

        return (
            jsonify(
                {
                    "success": False,
                    "message": f"Error occured during the follow process: {str(err)}",
                }
            ),
            500,
        )
    else:
        return (
            jsonify(
                {
                    "success": True,
                    "message": f"{follower_id} successfully follows {followed_id}",
                }
            ),
            201,
        )
