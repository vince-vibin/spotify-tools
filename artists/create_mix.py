""" create a mix for an artist you want """
#!/usr/bin/python3

import json
import sys
import traceback

import dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import models.artist_mix

dotenv.load_dotenv("../.env")

SCOPE = "playlist-modify-public"
Spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
USER = Spotify.current_user()["id"]
ArtistMix = models.artist_mix.ArtistMix

def error_handle(exctype, value, tb):
    tb_str = ''.join(traceback.format_exception(exctype, value, tb))
    print(tb_str)
    print("🆘 | Oh no, an error accured")
    print("Please try using --help an check your arguments")
    print("If this keeps happening feel free to open an issue here \n https://github.com/vince-vibin/spotify-tools/issues/new")

sys.excepthook = error_handle

def get_tracks(artist: dict):
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


def add2playlist(playlist: str, tracks: list):
    # You can add a maximum of 100 tracks per request.
    if len(tracks) > 100:
        while len(tracks) > 100:
            tracks_splitted = tracks[:100]
            del tracks[:100]
            Spotify.user_playlist_add_tracks(USER, playlist, tracks_splitted)
        Spotify.user_playlist_add_tracks(USER, playlist, tracks)
        return
    Spotify.user_playlist_add_tracks(USER, playlist, tracks)


def create(artist_mix: ArtistMix) -> None:
    artist = json.dumps(Spotify.artist(artist_mix.artist_link))
    artist = json.loads(artist)

    artist_name = artist["name"]
    if artist_mix.playlist_name is None:
        playlist_name = f"{artist_name} Mix"
    else:
        playlist_name = artist_mix.playlist_name

    print(f"🫡  | Creating Mix for artist {artist_name} as {playlist_name}...")
    playlist = Spotify.user_playlist_create(user=USER,
                                name=playlist_name,
                                public=True,
                                collaborative=False,
                                description=artist_mix.playlist_description)

    tracks = get_tracks(artist)
    add2playlist(playlist["id"], tracks)

    print(f"🎵 | {len(tracks)} Songs added.")
    print(f"✅ | Playlist created at https://open.spotify.com/playlist/{playlist['id']}")
    print("🙂 | Have Fun!")

    return {"message": f"https://open.spotify.com/playlist/{playlist['id']}"}
