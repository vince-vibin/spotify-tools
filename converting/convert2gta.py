""" Import your Spotify Playlist to GTA V Self Radio"""
#!/usr/bin/python3

import argparse
import json
import os

import dotenv
import pytube
import spotipy
from moviepy.editor import AudioFileClip
from mutagen.easyid3 import EasyID3
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
        print("🥲 | Given GTA Music Path not found")


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
    filename = f"{title[0].replace('.', '')}.webm".replace(':', '')
    s = pytube.Search(search)
    video = s.results[0]
    for stream in video.streams.filter(only_audio=True):
        if stream.abr == "70kbps" and stream.mime_type == "audio/webm":
            print(f"🔍 | Matching Stream found, downloading {search} now...")
            stream.download(output_path=f"{args.gta_musicfolder}{playlist['name']}/", filename=filename)
            convert_file(title[0], title[1], filename)
        else:
            print("🥲  | Matching Stream found but Bitrate or Audio Stream not matching")


def convert_file(songname, artist, filename):
    print("🔃 | Converting file and adding metadata...")
    filename_mp3 = filename.split(".webm")[0] + ".mp3"
    metadata ={
        'artist': artist,
        'title': songname,
    }
    webm = AudioFileClip(filename)
    webm.write_audiofile(filename_mp3, codec="libmp3lame")
    os.remove(filename)
    # add metadata
    audio = EasyID3(filename_mp3)
    for key, value in metadata.items():
        audio[key] = value
    audio.save()
    print(f"🥳 | Successfully downloaded and converted {songname} by {artist}")


if __name__ == "__main__":
    create_folder()
    track_titles = get_tracks_in_playlist(playlist["id"])
    for track in track_titles:
        yt_download(track)
    print(f"✅ | Finished! Checkout the files at {args.gta_musicfolder} \n \
    For a guide on how to enable Self Radio in GTA V checkout: \n \
        https://www.rockstargames.com/newswire/article/25o2411812a799/self-radio-create-your-own-custom-radio-station-in-gtav-pc")
