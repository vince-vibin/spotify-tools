""" Model definition for GtaRadio """
from pydantic import BaseModel


class GtaRadio(BaseModel):
    playlist_link: str
    folder_path: str
