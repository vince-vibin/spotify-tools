""" create a mix for an artist you want """

import argparse
import json

import dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

dotenv.load_dotenv("../.env")

SCOPE = "playlist-modify-public"
Spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
USER = Spotify.current_user()["id"]

parser = argparse.ArgumentParser(
                    prog="create artist mix",
                    description="Create a Mix for any artist you want",
                    epilog='For a full documentation check out the ReadMe')
parser.add_argument("artist_link",
                    help="The link to the profile of the artist you want to create a mix for")
parser.add_argument("--name",
                    help="The name of the mix playlist")
parser.add_argument("--size",
                    help="The number of songs in the mix (default is all songs)",
                    default=all)

args = parser.parse_args()

artist = json.dumps(Spotify.artist(args.artist_link))
artist = json.loads(artist)

def get_releases():
    page = Spotify.artist_albums(artist["id"], album_type=None, country=None, limit=50, offset=0)
    releases = page['items']
    while page['next']:
        page = Spotify.next(page)
        releases.extend(page['items'])
    return releases

if __name__ == "__main__":
    if args.name is None:
        artist_name = artist["name"]
        playlist_name = f"{artist_name} mix"
    else:
        playlist_name = args.name

    tracks = []
    for release in get_releases():
        if int(release["total_tracks"]) > 1:
            for song in Spotify.album_tracks(album_id=release["id"])["items"]:
                tracks.append(song["id"])
        elif release["album_type"] == "single":
            tracks.append(release["id"])

    playlist = Spotify.user_playlist_create(user=USER,
                                name=playlist_name,
                                public=True,
                                collaborative=False,
                                description="Custom Artist mix created using a script")

    Spotify.user_playlist_add_tracks(USER, playlist["id"], tracks)
