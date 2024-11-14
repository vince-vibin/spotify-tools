""" Convert your Spotify Playlist to local MP3s """
#!/usr/bin/python3

import json
import os
import sys
import traceback

import dotenv
import spotipy
from pytubefix import Search, YouTube
from spotipy.oauth2 import SpotifyOAuth

import models.mp3

dotenv.load_dotenv("../.env")

SCOPE = "playlist-read-private"
Spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
USER = Spotify.current_user()["id"]
Mp3 = models.mp3.Mp3

def error_handle(exctype, value, tb):
    tb_str = ''.join(traceback.format_exception(exctype, value, tb))
    print(tb_str)
    print("🆘 | Oh no, an error accured \n \
    Please try using --help an check your arguments \n \
    If this keeps happening feel free to open an issue here (Make sure to also give the error message) \n https://github.com/vince-vibin/spotify-tools/issues/new")

sys.excepthook = error_handle

# TODO this can be done by returning the path and using it as input for other functions then you dont need to change dir
def create_folder(playlist_name: str, folder: str):
    if os.path.exists(f"{folder}{playlist_name}/"):
        os.chdir(f"{folder}{playlist_name}/")
    elif os.path.exists(f"{folder}/"):
        os.chdir(f"{folder}/")
        os.mkdir(playlist_name)
        os.chdir(playlist_name)
    else:
        print("🥲 | Given Music Path not found")
    return f"{folder}/{playlist_name}/"


def get_tracks_in_playlist(playlist):
    print("⚒️  | Getting tracks from Playlist...")
    page = Spotify.playlist_tracks(playlist, limit=100)
    tracks = page['items']
    while page['next']:
        page = Spotify.next(page)
        tracks.extend(page['items'])
    temp = []
    for track in tracks:
        track = track["track"]
        temp.append([track['name'], track['artists'][0]['name']])
    tracks = temp
    return tracks


def yt_download(title: str, folder: str):
    search = f"{title[0]} {title[1]}"
    s = Search(search)
    url = s.videos[0].watch_url
    video = YouTube(url).streams.get_audio_only()
    print(f"🔍 | Matching Stream found, downloading {search} now...")
    video.download(mp3=True, filename_prefix=folder, filename=f"{search}")


def create(mp3: Mp3):
    playlist = json.dumps(Spotify.playlist(mp3.playlist_link))
    playlist = json.loads(playlist)

    musicfolder = create_folder(playlist['name'], mp3.folder_path)
    if not musicfolder.endswith("/"):
        musicfolder = musicfolder + "/"

    create_folder(playlist['name'], musicfolder)

    track_titles = get_tracks_in_playlist(playlist["id"])
    for track in track_titles:
        yt_download(track, musicfolder)
    print(f"✅ | Finished! Checkout the files at {musicfolder}")

    return {"message": f"{musicfolder}"}
