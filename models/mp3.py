""" Model definition for Mp3 """
from pydantic import BaseModel


class Mp3(BaseModel):
    playlist_link: str
    folder_path: str
