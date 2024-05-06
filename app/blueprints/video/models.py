import enum
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from app.app import db


class VideoStatus(enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class Video(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status: Mapped[VideoStatus] = mapped_column(
        default=VideoStatus.ACTIVE, nullable=False
    )

    @classmethod
    def create_video(cls, title: str, description: str, status: VideoStatus):
        """Create new video

        Args:
            video_id (int): Video id
            title (str): Video title
            description (str): Video description
            status (VideoStatus): Video status

        Returns:
            video: Video object
        """
        video = cls(title=title, description=description, status=VideoStatus(status))
        db.session.add(video)
        db.session.commit()
        return video

    @classmethod
    def get_videos(cls):
        """Return all videos

        Returns:
            videos: Video objects
        """
        return cls.query.all()

    @classmethod
    def get_videos_by_status(cls, status: VideoStatus):
        """Return all videos by status

        Args:
            status (VideoStatus): Video status

        Returns:
            videos: Video objects
        """
        return cls.query.filter_by(status=status.upper()).all()

    @classmethod
    def get_video(cls, video_id: int):
        """Return a video by id

        Args:
            video_id (int): Video id

        Returns:
            videos: Video objects
        """
        return cls.query.get(video_id)

    @classmethod
    def update_video(
        cls, video_id: int, title: str, description: str, status: VideoStatus
    ):
        """Update video by id

        Args:
            video_id (int): Video id
            title (str): Video title
            description (str): Video description
            status (VideoStatus): Video status

        Returns:
            video: Video object
        """
        video = cls.query.get(video_id)
        video.title = title
        video.description = description
        video.status = VideoStatus(status) if status else video.status
        db.session.commit()
        return video

    @classmethod
    def delete_video(cls, video_id: int):
        """Delete video by id

        Args:
            video_id (int): Video id

        Returns:
            video: Video object
        """
        video = cls.query.get(video_id)
        if not video:
            return None
        db.session.delete(video)
        db.session.commit()
        return video

    def to_json(self):
        """Convert Video object to JSON

        Returns:
            dict: Video object as JSON
        """
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            status=self.status.value.lower(),
            created_at=self.created_at.isoformat(),
        )

    def __repr__(self):
        return f"Video {self.title}"
