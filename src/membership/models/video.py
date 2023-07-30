from uuid import uuid4
from typing import Optional

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from membership.core.config import settings
from membership.models.user import UserModel
from membership.utils.extract import get_video_id_from_url
from membership.exceptions.video import VideoAlreadyExistError


class VideoModel(Model):
    __keyspace__ = settings.CASSANDRA_DB_KEYSPACE

    youtube_id = columns.Text(primary_key=True)
    youtube_url = columns.Text()

    video_id = columns.UUID(default=uuid4())
    user_email = columns.Text()

    def __repr__(self) -> str:
        return f"VideoModel(youtube_id={self.youtube_id}, user_email={self.user_email})"
    
    @classmethod
    def create_video(cls, youtube_url: str, user: UserModel) -> 'VideoModel':
        video_yid = get_video_id_from_url(youtube_url)

        if cls.get_video_by_yid(video_yid):
            raise VideoAlreadyExistError
        
        return VideoModel.create(
            youtube_id=video_yid,
            youtube_url=youtube_url,
            user_email=user.email
        )
        
    @classmethod
    def get_video_by_yid(cls, youtube_id: str) -> Optional['VideoModel']:
        qset = VideoModel.objects.filter(youtube_id=youtube_id)
        return qset.first()