import pytest

from membership.core.db import get_cdb
from membership.models.user import UserModel
from membership.models.video import VideoModel
from membership.exceptions.video import InvalidYoutubeUrlError, VideoAlreadyExistError

@pytest.fixture
def initialization():
    get_cdb()
    user = UserModel(email="aviregmi2018@gmail.com", hpassword="jibbrish")
    return {
        "user": user
    }


def test_video_creation_wrong_url(initialization):
    with pytest.raises(InvalidYoutubeUrlError):
        VideoModel.create_video(youtube_url="abhinasregmi123", user=initialization['user'])

def test_video_creation_correct_url(initialization):
    video = VideoModel.create_video(
        youtube_url="https://www.youtube.com/watch?v=KQ-u4RcFLBY&t=15041s&ab_channel=CodingEntrepreneurs",
        user=initialization['user']
        )
    
    assert isinstance(video, VideoModel)

    video.delete()



def test_video_creation_multiple(initialization):
    try:
        video1 = VideoModel.create_video(
        youtube_url="https://www.youtube.com/watch?v=KQ-u4RcFLBY&t=15041s&ab_channel=CodingEntrepreneurs",
        user=initialization['user']
        )

        video2 = VideoModel.create_video(
        youtube_url="https://www.youtube.com/watch?v=KQ-u4RcFLBY&t=15041s&ab_channel=CodingEntrepreneurs",
        user=initialization['user']
        )
    except VideoAlreadyExistError:
        assert True

        video1.delete() #type:ignore