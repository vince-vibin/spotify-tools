""" controller script taking api calls """
from fastapi import FastAPI

import artists.create_mix
import converting.gta
import converting.mp3
import models.artist_mix
import models.gta_radio
import models.mp3

spotify_tools = FastAPI()

ArtistMix = models.artist_mix.ArtistMix
GtaRadio = models.gta_radio.GtaRadio
Mp3 = models.mp3.Mp3

# TODO Centralize Authentification
# TODO Implement a utils class with common functions
# TODO Clean Up code after Fast API changes
# TODO Implement a Logging libary
# TODO Implement Metrics



@spotify_tools.get("/")
async def root():
    return {"message": "Hello World"}


@spotify_tools.post("/artists/create_mix")
async def create_artist_mix(artist_mix: ArtistMix):
    return artists.create_mix.create(artist_mix)


@spotify_tools.post("/converting/gta")
async def convert_to_gta(gta_radio: GtaRadio):
    return converting.gta.create(gta_radio)

@spotify_tools.post("/converting/mp3")
async def convert_to_mp3(mp3: Mp3):
    return converting.mp3.create(mp3)
