""" Import your Spotify Playlist to GTA V """

import argparse
import json
import os

import dotenv
import pytube
import spotipy
from spotipy.oauth2 import SpotifyOAuth

dotenv.load_dotenv("../.env")

SCOPE = "playlist-read-private"
Spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
USER = Spotify.current_user()["id"]

parser = argparse.ArgumentParser(
                    prog="import to gta v",
                    description="Import your Spotify Playlist to GTA V",
                    epilog='For a full documentation check out the ReadMe')
parser.add_argument("playlist_link",
                    help="The link to the playlist you want to convert")
parser.add_argument("gta_musicfolder",
                    help="The full path to your GTA Music Folder (usually something like C:/Users/<USERNAME>/OneDrive/Dokumente/Rockstar Games/GTA V/User Music)")
args = parser.parse_args()

playlist = json.dumps(Spotify.playlist(args.playlist_link))
playlist = json.loads(playlist)

if not args.gta_musicfolder.endswith("/"):
    args.gta_musicfolder = args.gta_musicfolder + "/"

def create_folder():
    if os.path.exists(f"{args.gta_musicfolder}{playlist['name']}/"):
        os.chdir(f"{args.gta_musicfolder}{playlist['name']}/")
    elif os.path.exists(f"{args.gta_musicfolder}/"):
        os.chdir(f"{args.gta_musicfolder}/")
        os.mkdir(playlist['name'])
        os.chdir(playlist['name'])
    else:
        print("Given GTA Music Path not found")


def get_tracks_in_playlist(playlist):
    page = Spotify.playlist_tracks(playlist, limit=100)
    tracks = page['items']
    while page['next']:
        page = Spotify.next(page)
        tracks.extend(page['items'])
    temp = []
    for track in tracks:
        track = track["track"]
        temp.append(f"{track['name']} {track['artists'][0]['name']}")
    tracks = temp
    return tracks


def yt_download(title):
    s = pytube.Search(title)
    video = s.results[0]
    for stream in video.streams.filter(only_audio=True):
        if stream.abr == "70kbps" and stream.mime_type == "audio/webm":
            print("Matching Stream found, downloading now...")
            stream.download(output_path=f"{args.gta_musicfolder}{playlist['name']}/")
        else:
            print("Matching Bitrate or Audio Stream not found")


def convert_files():
    playlist_folder = os.fspath(args.gta_musicfolder + playlist['name'])
    for file in os.listdir(playlist_folder):
        if file != ".cache":
            base, ext = file.split(".")
            os.rename(file, f"{base}.mp3")

if __name__ == "__main__":
    create_folder()
    track_titles = get_tracks_in_playlist(playlist["id"])
    for track in track_titles:
        yt_download(track)
    convert_files()