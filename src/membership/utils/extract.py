import re

from membership.exceptions.video import InvalidYoutubeUrlError

def get_video_id_from_url(url:str ) -> str:
   data = re.findall(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
   
   if data:
      return data[0]
   
   raise InvalidYoutubeUrlError