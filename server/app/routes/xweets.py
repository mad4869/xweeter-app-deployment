from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from minio.error import S3Error
from datetime import datetime

from . import routes
from ..extensions import db, mc
from ..models import Xweet, User, Hashtag, hashtag_xweet
from ..constants import MINIO_BUCKET
from ..utils.manage_file import manage_file


@routes.route("/xweets/<int:xweet_id>", methods=["GET"], strict_slashes=False)
def get_xweet(xweet_id):
    xweet = db.session.execute(
        db.select(Xweet).filter(Xweet.xweet_id == xweet_id)
    ).scalar_one_or_none()

    if xweet is None:
        return jsonify({"success": False, "message": "Xweet is not found"}), 404

    data = xweet.serialize()
    data.update(
        {
            "username": xweet.users.username,
            "full_name": xweet.users.full_name,
            "profile_pic": xweet.users.profile_pic,
        }
    )

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/<int:user_id>/xweets", methods=["GET"], strict_slashes=False)
def get_xweets_by_user(user_id):
    xweets = db.session.execute(
        db.select(Xweet)
        .join(User, Xweet.user_id == User.user_id)
        .filter(User.user_id == user_id)
        .order_by(Xweet.created_at.desc())
    ).scalars()
    data = []
    for xweet in xweets:
        serial = xweet.serialize()
        serial.update(
            {
                "username": xweet.users.username,
                "full_name": xweet.users.full_name,
                "profile_pic": xweet.users.profile_pic,
            }
        )
        data.append(serial)

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/<int:user_id>/xweets", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_xweet(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"success": False, "message": "Unauthorized action"}), 403

    body = request.form.get("body", "")
    media = request.files.get("media", None)
    media_name = None
    media_updated_at = None
    hashtags = request.form.getlist("hashtags")

    if not body and not media:
        return (
            jsonify({"success": False, "message": "Xweet cannot be empty"}),
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

    xweet = Xweet(
        user_id=user_id,
        body=body,
        media=media,
        media_name=media_name,
        media_updated_at=media_updated_at,
    )

    try:
        db.session.add(xweet)
        db.session.commit()

        if len(hashtags) != 0:
            for tag in hashtags:
                existing_tag_same_xweet = db.session.execute(
                    db.select(Hashtag)
                    .join(
                        hashtag_xweet, Hashtag.hashtag_id == hashtag_xweet.c.hashtag_id
                    )
                    .filter(
                        Hashtag.body == tag, hashtag_xweet.c.xweet_id == xweet.xweet_id
                    )
                ).scalar_one_or_none()

                if existing_tag_same_xweet:
                    continue

                existing_tag = db.session.execute(
                    db.select(Hashtag).filter(Hashtag.body == tag)
                ).scalar_one_or_none()

                if existing_tag:
                    db.session.execute(
                        hashtag_xweet.insert().values(
                            xweet_id=xweet.xweet_id,
                            hashtag_id=existing_tag.hashtag_id,
                        )
                    )
                    db.session.commit()
                else:
                    hashtag = Hashtag(body=tag)

                    db.session.add(hashtag)
                    db.session.commit()

                    db.session.execute(
                        hashtag_xweet.insert().values(
                            xweet_id=xweet.xweet_id, hashtag_id=hashtag.hashtag_id
                        )
                    )
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
        return jsonify({"success": True, "data": xweet.serialize()}), 201


@routes.route(
    "/users/<int:user_id>/xweets/<int:xweet_id>",
    methods=["PUT", "DELETE"],
    strict_slashes=False,
)
@jwt_required()
def access_xweet_by_user(user_id, xweet_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"success": False, "message": "Unauthorized action"}), 403

    xweet = db.session.execute(
        db.select(Xweet).filter(Xweet.xweet_id == xweet_id)
    ).scalar_one_or_none()

    if xweet is None:
        return (
            jsonify({"success": False, "message": "Xweet not found"}),
            404,
        )

    if request.method == "PUT":
        new_body = request.form.get("new_body", "")
        new_media = request.files.get("new_media", None)
        new_media_name = None
        new_media_updated_at = None
        new_media_url = request.form.get("new_media_url", "")
        hashtags = request.form.getlist("hashtags")

        if not new_body and not new_media:
            return (
                jsonify({"success": False, "message": "Xweet cannot be empty"}),
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
                new_media = xweet.media

        try:
            xweet.body = new_body
            xweet.media = new_media
            xweet.media_name = new_media_name
            xweet.media_updated_at = new_media_updated_at
            xweet.updated_at = datetime.now()
            db.session.commit()

            if len(hashtags) != 0:
                for tag in hashtags:
                    existing_tag_same_xweet = db.session.execute(
                        db.select(Hashtag)
                        .join(
                            hashtag_xweet,
                            Hashtag.hashtag_id == hashtag_xweet.c.hashtag_id,
                        )
                        .filter(
                            Hashtag.body == tag,
                            hashtag_xweet.c.xweet_id == xweet.xweet_id,
                        )
                    ).scalar_one_or_none()

                    if existing_tag_same_xweet:
                        continue

                    existing_tag = db.session.execute(
                        db.select(Hashtag).filter(Hashtag.body == tag)
                    ).scalar_one_or_none()

                    if existing_tag:
                        db.session.execute(
                            hashtag_xweet.insert().values(
                                xweet_id=xweet.xweet_id,
                                hashtag_id=existing_tag.hashtag_id,
                            )
                        )
                        db.session.commit()
                    else:
                        hashtag = Hashtag(body=tag)

                        db.session.add(hashtag)
                        db.session.commit()

                        db.session.execute(
                            hashtag_xweet.insert().values(
                                xweet_id=xweet.xweet_id, hashtag_id=hashtag.hashtag_id
                            )
                        )
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
            return jsonify({"success": True, "data": xweet.serialize()}), 201

    elif request.method == "DELETE":
        try:
            db.session.delete(xweet)
            db.session.commit()
        except:
            db.session.rollback()

            return (
                jsonify({"success": False, "message": "Failed to delete the xweet"}),
                500,
            )
        else:
            return (
                jsonify({"success": True, "data": xweet.serialize()}),
                201,
            )

    return jsonify({"success": True, "data": xweet.serialize()}), 200
