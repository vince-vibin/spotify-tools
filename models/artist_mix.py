""" Model definition for ArtistMix """
from pydantic import BaseModel


class ArtistMix(BaseModel):
    playlist_name: str = None
    artist_link: str
    playlist_description: str = "Custom Artist mix created using a script"
