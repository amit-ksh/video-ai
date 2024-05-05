from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from .models import Video

video_bp = Blueprint("video", __name__)


@video_bp.route("/videos", methods=["GET"])
def get_all_videos():
    all_videos = Video.get_videos()

    return [video.to_json() for video in all_videos]


@video_bp.route("/video/<int:video_id>", methods=["GET"])
def get_video(video_id):
    video = Video.get_video(video_id)

    if not video:
        return "Video not found", 404

    return video.to_json()


@video_bp.route("/videos/<status>", methods=["GET"])
def get_videos_by_status(status):
    all_videos = Video.get_videos_by_status(status)

    return [video.to_json() for video in all_videos]


@video_bp.route("/video", methods=["POST"])
@jwt_required()
def create_video():
    title = request.json.get("title")
    description = request.json.get("description")
    status = request.json.get("status")

    if not title or not description:
        return {"message": "Title and description are required"}, 400

    return Video.create_video(title, description, status).to_json()


@video_bp.route("/video/<int:video_id>", methods=["PUT"])
@jwt_required()
def update_video(video_id):
    title = request.json.get("title")
    description = request.json.get("description")
    status = request.json.get("status", None)

    if not title or not description:
        return {"message": "Title and description are required"}, 400

    video = Video.update_video(video_id, title, description, status)

    return video.to_json()


@video_bp.route("/video/<int:video_id>", methods=["DELETE"])
@jwt_required()
def delete_video(video_id):
    video = Video.delete_video(video_id)

    if not video:
        return "Video not found", 404

    return video.to_json()
