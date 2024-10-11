""" create a mix for an artist you want """
#!/usr/bin/python3

import argparse
import json
import sys
import traceback

import dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

dotenv.load_dotenv("../.env")

SCOPE = "playlist-modify-public"
Spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
USER = Spotify.current_user()["id"]

def error_handle(exctype, value, tb):
    tb_str = ''.join(traceback.format_exception(exctype, value, tb))
    print(tb_str)
    print("🆘 | Oh no, an error accured")
    print("Please try using --help an check your arguments")
    print("If this keeps happening feel free to open an issue here \n https://github.com/vince-vibin/spotify-tools/issues/new")

sys.excepthook = error_handle

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
                    default="all")
parser.add_argument("--mode",
                    help="The mode of the mix",
                    default="none")
args = parser.parse_args()

artist = json.dumps(Spotify.artist(args.artist_link))
artist = json.loads(artist)

def get_tracks():
    tracks = []

    # get albums
    albums = Spotify.artist_albums(artist["id"], album_type="album", country=None, limit=20, offset=0)
    releases_albums = albums['items']
    while albums['next']:
        albums = Spotify.next(albums)
        releases_albums.extend(albums['items'])

    for album in releases_albums:
        for song in Spotify.album_tracks(album_id=album["id"])["items"]:
            tracks.append([song["id"], song["name"]])

    # get singles
    singles = Spotify.artist_albums(artist["id"], album_type="single", country=None, limit=20, offset=0)
    releases_singels = singles['items']
    while singles['next']:
        singles = Spotify.next(singles)
        releases_singels.extend(singles['items'])

    for single in releases_singels:
        for song in Spotify.album_tracks(album_id=single["id"])["items"]:
            tracks.append([song["id"], song["name"]])

    # tracks that are later added to an album get a new id so we need to check by name
    names = []
    temp = []
    for track in tracks:
        if track[1] not in names:
            temp.append(track[0])
            names.append(track[1])
    tracks = temp

    return tracks

def add2playlist(playlist, tracks):
    # You can add a maximum of 100 tracks per request.
    if len(tracks) > 100:
        while len(tracks) > 100:
            tracks_splitted = tracks[:100]
            del tracks[:100]
            Spotify.user_playlist_add_tracks(USER, playlist, tracks_splitted)
        Spotify.user_playlist_add_tracks(USER, playlist, tracks)
        return
    Spotify.user_playlist_add_tracks(USER, playlist, tracks)

if __name__ == "__main__":
    artist_name = artist["name"]
    if args.name is None:
        PLAYLIST_NAME = f"{artist_name} Mix"
    else:
        PLAYLIST_NAME = args.name

    print(f"🫡  | Creating Mix for artist {artist_name} as {PLAYLIST_NAME}...")
    playlist = Spotify.user_playlist_create(user=USER,
                                name=PLAYLIST_NAME,
                                public=True,
                                collaborative=False,
                                description="Custom Artist mix created using a script")

    tracks = get_tracks()
    add2playlist(playlist["id"], tracks)

    print(f"🎵 | {len(tracks)} Songs added.")
    print(f"✅ | Playlist created at https://open.spotify.com/playlist/{playlist['id']}")
    print("🙂 | Have Fun!")
