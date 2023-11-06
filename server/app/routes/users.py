from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from minio.error import S3Error
from datetime import datetime
import json

from . import routes
from ..extensions import db, mc
from ..models import User, Xweet
from ..constants import MINIO_BUCKET
from ..utils.manage_file import manage_file


@routes.route("/users/most-active", methods=["GET"], strict_slashes=False)
def get_most_active_users():
    most_active_users = (
        db.session.query(
            User.user_id,
            User.username,
            User.full_name,
            User.profile_pic,
            db.func.count(Xweet.xweet_id).label("xweet_count"),
        )
        .join(Xweet, User.user_id == Xweet.user_id)
        .group_by(User.user_id, User.username, User.full_name)
        .order_by(db.func.count(Xweet.xweet_id).desc())
        .limit(2)
        .subquery()
    )
    most_active_users_xweets = (
        db.session.query(
            Xweet.body,
            most_active_users.c.user_id,
            most_active_users.c.username,
            most_active_users.c.full_name,
            most_active_users.c.profile_pic,
            db.func.row_number()
            .over(partition_by=Xweet.user_id, order_by=Xweet.created_at.desc())
            .label("row_num"),
        )
        .join(most_active_users, Xweet.user_id == most_active_users.c.user_id)
        .order_by(most_active_users.c.xweet_count)
        .subquery()
    )
    most_active_users_last_xweets = db.session.execute(
        db.select(
            most_active_users_xweets.c.body,
            most_active_users_xweets.c.user_id,
            most_active_users_xweets.c.username,
            most_active_users_xweets.c.full_name,
            most_active_users_xweets.c.profile_pic,
        ).filter(most_active_users_xweets.c.row_num == 1)
    ).fetchall()
    data = [
        {
            "body": user[0],
            "user_id": user[1],
            "username": user[2],
            "full_name": user[3],
            "profile_pic": user[4],
        }
        for user in most_active_users_last_xweets
    ]

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/most-active-daily", methods=["GET"], strict_slashes=False)
def get_daily_top_users():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    query = (
        db.session.query(
            User.user_id,
            User.username,
            User.full_name,
            db.func.count(Xweet.xweet_id).label("xweet_count"),
        )
        .join(Xweet)
        .filter(db.func.date(Xweet.created_at) == db.func.date(db.func.now()))
        .group_by(User.user_id, User.username, User.full_name)
        .order_by(db.func.count(Xweet.xweet_id).desc())
    )

    results = query.paginate(page=page, per_page=per_page)

    users = [
        {
            "user_id": user.user_id,
            "username": user.username,
            "full_name": user.full_name,
            "xweet_count": user.xweet_count,
        }
        for user in results.items
    ]

    data = {
        "users": users,
        "total_pages": results.pages,
        "total_users": results.total,
    }

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/<int:user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    user = db.session.execute(
        db.select(User).filter(User.user_id == user_id)
    ).scalar_one_or_none()

    if user is None:
        return jsonify({"success": False, "message": "User is not found"}), 404

    data = user.serialize()

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/<int:user_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"success": False, "message": "Unauthorized action"}), 403

    user = db.session.execute(
        db.select(User).filter(User.user_id == user_id)
    ).scalar_one_or_none()

    if user is None:
        return jsonify({"success": False, "message": "User is not found"}), 404

    updated_username = request.form.get("username", user.username)
    updated_full_name = request.form.get("fullname", user.full_name)
    updated_email = request.form.get("email", user.email)
    updated_bio = request.form.get("bio", user.bio)
    updated_profile_pic = request.files.get("profile_pic")
    updated_profile_pic_name = None
    updated_profile_pic_updated_at = None
    updated_header_pic = request.files.get("header_pic")
    updated_header_pic_name = None
    updated_header_pic_updated_at = None

    if updated_profile_pic:
        updated_profile_pic_name, updated_profile_pic_size = manage_file(
            updated_profile_pic
        )

        try:
            bucket_existing = mc.bucket_exists(MINIO_BUCKET)
            if not bucket_existing:
                mc.make_bucket(MINIO_BUCKET)
            mc.put_object(
                MINIO_BUCKET,
                updated_profile_pic_name,
                updated_profile_pic,
                updated_profile_pic_size,
            )
            updated_profile_pic = mc.presigned_get_object(
                MINIO_BUCKET, updated_profile_pic_name
            )
            updated_profile_pic_updated_at = datetime.now()
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
        updated_profile_pic = user.profile_pic
        updated_profile_pic_name = user.profile_pic_name
        updated_profile_pic_updated_at = user.profile_pic_updated_at

    if updated_header_pic:
        updated_header_pic_name, updated_header_pic_size = manage_file(
            updated_header_pic
        )
        try:
            bucket_existing = mc.bucket_exists(MINIO_BUCKET)
            if not bucket_existing:
                mc.make_bucket(MINIO_BUCKET)
            mc.put_object(
                MINIO_BUCKET,
                updated_header_pic_name,
                updated_header_pic,
                updated_header_pic_size,
            )
            updated_header_pic = mc.presigned_get_object(
                MINIO_BUCKET, updated_header_pic_name
            )
            updated_header_pic_updated_at = datetime.now()
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
        updated_header_pic = user.header_pic
        updated_header_pic_name = user.header_pic_name
        updated_header_pic_updated_at = user.header_pic_updated_at

    try:
        user.username = updated_username
        user.full_name = updated_full_name
        user.email = updated_email
        user.bio = updated_bio
        user.profile_pic = updated_profile_pic
        user.profile_pic_name = updated_profile_pic_name
        user.profile_pic_updated_at = updated_profile_pic_updated_at
        user.header_pic = updated_header_pic
        user.header_pic_name = updated_header_pic_name
        user.header_pic_updated_at = updated_header_pic_updated_at
        user.updated_at = datetime.now()

        db.session.commit()
    except:
        db.session.rollback()

        return (
            jsonify({"success": False, "message": "Failed to update the profile"}),
            500,
        )
    else:
        updated_data = user.serialize()

        return jsonify({"success": True, "data": updated_data}), 201
