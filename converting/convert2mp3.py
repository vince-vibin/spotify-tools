""" Convert your Spotify Playlist to local MP3s """
#!/usr/bin/python3

import argparse
import json
import os
import sys
import traceback

import dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from pytubefix import YouTube, Search

dotenv.load_dotenv("../.env")

SCOPE = "playlist-read-private"
Spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
USER = Spotify.current_user()["id"]

def error_handle(exctype, value, tb):
    tb_str = ''.join(traceback.format_exception(exctype, value, tb))
    print(tb_str)
    print("🆘 | Oh no, an error accured \n \
    Please try using --help an check your arguments \n \
    If this keeps happening feel free to open an issue here (Make sure to also give the error message) \n https://github.com/vince-vibin/spotify-tools/issues/new")

sys.excepthook = error_handle

parser = argparse.ArgumentParser(
                    prog="Convert to gta v",
                    description="Convert your Spotify Playlist to local MP3s",
                    epilog='For a full documentation check out the ReadMe')
parser.add_argument("playlist_link",
                    help="The link to the playlist you want to convert")
parser.add_argument("musicfolder",
                    help="The full path to your Music Folder (something like C:/Users/<USERNAME>/Music/my-playlist/)")
args = parser.parse_args()

playlist = json.dumps(Spotify.playlist(args.playlist_link))
playlist = json.loads(playlist)

if not args.musicfolder.endswith("/"):
    args.musicfolder = args.musicfolder + "/"

def create_folder():
    if os.path.exists(f"{args.musicfolder}{playlist['name']}/"):
        os.chdir(f"{args.musicfolder}{playlist['name']}/")
    elif os.path.exists(f"{args.musicfolder}/"):
        os.chdir(f"{args.musicfolder}/")
        os.mkdir(playlist['name'])
        os.chdir(playlist['name'])
    else:
        print("🥲 | Given Music Path not found")


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


def yt_download(title):
    search = f"{title[0]} {title[1]}"
    s = Search(search)
    url = s.videos[0].watch_url
    video = YouTube(url).streams.get_audio_only()
    print(f"🔍 | Matching Stream found, downloading {search} now...")
    video.download(mp3=True, filename_prefix=args.musicfolder, filename=f"{search}")


if __name__ == "__main__":
    create_folder()
    track_titles = get_tracks_in_playlist(playlist["id"])
    for track in track_titles:
        yt_download(track)
    print(f"✅ | Finished! Checkout the files at {args.musicfolder}")
