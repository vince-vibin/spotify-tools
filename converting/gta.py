""" Import your Spotify Playlist to GTA V Self Radio """
#!/usr/bin/python3

import json
import os
import sys
import traceback

import dotenv
import spotipy
from pytubefix import Search, YouTube
from spotipy.oauth2 import SpotifyOAuth

import models.gta_radio

dotenv.load_dotenv("../.env")

SCOPE = "playlist-read-private"
Spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
USER = Spotify.current_user()["id"]
GtaRadio = models.gta_radio.GtaRadio

def error_handle(exctype, value, tb):
    tb_str = ''.join(traceback.format_exception(exctype, value, tb))
    print(tb_str)
    print("🆘 | Oh no, an error accured \n \
    Please try using --help an check your arguments \n \
    If this keeps happening feel free to open an issue here (Make sure to also give the error message) \n https://github.com/vince-vibin/spotify-tools/issues/new")

sys.excepthook = error_handle

def create_folder(playlist_name: str, folder: str):
    if os.path.exists(f"{folder}{playlist_name}/"):
        os.chdir(f"{folder}{playlist_name}/")
    elif os.path.exists(f"{folder}/"):
        os.chdir(f"{folder}/")
        os.mkdir(playlist_name)
        os.chdir(playlist_name)
    else:
        print("🥲 | Given GTA Music Path not found")
    return f"{folder}/{playlist_name}/"


def get_tracks_in_playlist(playlist):
    print("⚒️ | Getting tracks from Playlist...")
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
    if len(s.videos) > 0:
        url = s.videos[0].watch_url
        video = YouTube(url).streams.get_audio_only()
        print(f"🔍 | Matching Stream found, downloading {search} now...")
        video.download(mp3=True, filename_prefix=folder, filename=f"{search}")
    else:
        print("🥲 | Matching stream for {search} not found.")

def create(gta_radio: GtaRadio):
    playlist = json.dumps(Spotify.playlist(gta_radio.playlist_link))
    playlist = json.loads(playlist)

    folder = create_folder(playlist['name'], gta_radio.folder_path)

    if not folder.endswith("/"):
        folder = folder + "/"


    track_titles = get_tracks_in_playlist(playlist["id"])
    for track in track_titles:
        yt_download(track, folder)

    print(f"✅ | Finished! Checkout the files at {folder} \n \
    For a guide on how to enable Self Radio in GTA V checkout: \n \
        https://www.rockstargames.com/newswire/article/25o2411812a799/self-radio-create-your-own-custom-radio-station-in-gtav-pc")

    return {"message": f"{folder}"}
