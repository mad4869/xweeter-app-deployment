from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import emit
from minio.error import S3Error
from datetime import datetime

from . import routes
from ..extensions import db, mc, socket
from ..models import Xweet, User, Reply
from ..constants import MINIO_BUCKET
from ..utils.manage_file import manage_file


@socket.on("add_to_replies")
def add_to_replies(xweet_id):
    reply = db.session.execute(
        db.select(Reply)
        .join(Xweet, Reply.xweet_id == Xweet.xweet_id)
        .join(User, Xweet.user_id == User.user_id)
        .filter(Reply.xweet_id == xweet_id)
        .order_by(Reply.created_at.desc())
        .limit(1)
    ).scalar_one_or_none()
    reply_data = reply.serialize()
    reply_data["username"] = reply.users.username
    reply_data["full_name"] = reply.users.full_name
    reply_data["profile_pic"] = reply.users.profile_pic

    emit("add_to_replies", reply_data, broadcast=True)


@routes.route("/xweets/<int:xweet_id>/replies", methods=["GET"], strict_slashes=False)
def get_replies_by_xweet(xweet_id):
    start = int(request.args.get("start", 0))
    size = int(request.args.get("size", 10))

    replies = db.session.execute(
        db.select(Reply)
        .join(Xweet, Reply.xweet_id == Xweet.xweet_id)
        .join(User, Xweet.user_id == User.user_id)
        .filter(Reply.xweet_id == xweet_id)
        .order_by(Reply.created_at)
    ).scalars()

    data = []

    for reply in replies:
        serial = reply.serialize()
        serial.update(
            {
                "username": reply.users.username,
                "full_name": reply.users.full_name,
                "profile_pic": reply.users.profile_pic,
                "og_user_id": reply.xweets.users.user_id,
                "og_username": reply.xweets.users.username,
                "og_full_name": reply.xweets.users.full_name,
                "og_profile_pic": reply.xweets.users.profile_pic,
                "og_body": reply.xweets.body,
                "og_media": reply.xweets.media,
            }
        )
        data.append(serial)

    end = min(start + size, len(data))

    sliced_data = data[start:end]

    return jsonify({"success": True, "data": sliced_data}), 200


@routes.route("/users/<int:user_id>/replies", methods=["GET"], strict_slashes=False)
def get_replies_by_user(user_id):
    replies = db.session.execute(
        db.select(Reply)
        .join(Xweet, Reply.xweet_id == Xweet.xweet_id)
        .join(User, Reply.user_id == User.user_id)
        .filter(Reply.user_id == user_id)
        .order_by(Reply.created_at.desc())
    ).scalars()

    data = []

    for reply in replies:
        serial = reply.serialize()
        serial.update(
            {
                "username": reply.users.username,
                "full_name": reply.users.full_name,
                "profile_pic": reply.users.profile_pic,
                "og_user_id": reply.xweets.users.user_id,
                "og_username": reply.xweets.users.username,
                "og_full_name": reply.xweets.users.full_name,
                "og_profile_pic": reply.xweets.users.profile_pic,
                "og_body": reply.xweets.body,
                "og_media": reply.xweets.media,
            }
        )
        data.append(serial)

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/<int:user_id>/replies", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_reply(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"success": False, "message": "Unauthorized action"}), 403

    xweet_id = int(request.form.get("xweet_id"))
    body = request.form.get("body", "")
    media = request.files.get("media", None)
    media_name = None
    media_updated_at = None

    if not body and not media:
        return (
            jsonify({"success": False, "message": "Reply cannot be empty"}),
            400,
        )

    if media:
        media_name, media_size = manage_file(media)

        try:
            bucket_existing = mc.bucket_exists(MINIO_BUCKET)
            if not bucket_existing:
                mc.make_bucket(MINIO_BUCKET)
            mc.put_object(MINIO_BUCKET, media_name, media, media_size)
            media = mc.presigned_get_object(MINIO_BUCKET, media_name)
            media_updated_at = datetime.now()
        except S3Error as err:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": f"Error occured during the process: {str(err)}",
                    }
                ),
                500,
            )

    reply = Reply(
        user_id=user_id,
        xweet_id=xweet_id,
        body=body,
        media=media,
        media_name=media_name,
        media_updated_at=media_updated_at,
    )

    try:
        db.session.add(reply)
        db.session.commit()
    except:
        db.session.rollback()

        return (
            jsonify({"success": False, "message": "Failed to reply xweet"}),
            500,
        )
    else:
        return jsonify({"success": True, "data": reply.serialize()}), 201


@routes.route(
    "/users/<int:user_id>/replies/<int:reply_id>",
    methods=["PUT", "DELETE"],
    strict_slashes=False,
)
@jwt_required()
def access_reply_by_user(user_id, reply_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"success": False, "message": "Unauthorized action"}), 403

    reply = db.session.execute(
        db.select(Reply).filter(Reply.reply_id == reply_id)
    ).scalar_one_or_none()

    if reply is None:
        return (
            jsonify({"success": False, "message": "Reply not found"}),
            404,
        )

    if request.method == "PUT":
        new_body = request.form.get("new_body", "")
        new_media = request.files.get("new_media", None)
        new_media_name = None
        new_media_updated_at = None
        new_media_url = request.form.get("new_media_url", "")

        if not new_body and not new_media:
            return (
                jsonify({"success": False, "message": "Reply cannot be empty"}),
                400,
            )

        if new_media:
            new_media_name, new_media_size = manage_file(new_media)

            try:
                bucket_existing = mc.bucket_exists(MINIO_BUCKET)
                if not bucket_existing:
                    mc.make_bucket(MINIO_BUCKET)
                mc.put_object(MINIO_BUCKET, new_media_name, new_media, new_media_size)
                new_media = mc.presigned_get_object(MINIO_BUCKET, new_media_name)
                new_media_updated_at = datetime.now()
            except S3Error as err:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": f"Error occured during the process: {str(err)}",
                        }
                    ),
                    500,
                )
        else:
            if new_media_url:
                new_media = reply.media

        try:
            reply.body = new_body
            reply.media = new_media
            reply.media_name = new_media_name
            reply.media_updated_at = new_media_updated_at
            reply.updated_at = datetime.now()
            db.session.commit()
        except Exception as err:
            db.session.rollback()

            return (
                jsonify(
                    {
                        "success": False,
                        "message": f"Error occured during the process: {str(err)}",
                    }
                ),
                500,
            )
        else:
            return jsonify({"success": True, "data": reply.serialize()}), 201

    elif request.method == "DELETE":
        try:
            db.session.delete(reply)
            db.session.commit()
        except:
            db.session.rollback()

            return (
                jsonify({"success": False, "message": "Failed to delete the reply"}),
                500,
            )
        else:
            return (
                jsonify({"success": True, "data": reply.serialize()}),
                201,
            )

    return jsonify({"success": True, "data": reply.serialize()}), 200
