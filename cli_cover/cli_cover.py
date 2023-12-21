""" Script to print the cover of your current playing spotify song to the cli """
#!/usr/bin/python3

import json
import sys
import urllib

import dotenv
import PIL.Image
import spotipy
from spotipy.oauth2 import SpotifyOAuth

dotenv.load_dotenv("../.env")

SCOPE = "user-read-playback-state"
Spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))

# use two hashtags to get a square image
CHAR = "##"

# map spotify provided cover sources to its position in the json response
SIZES_MAP = {
    640: 0,
    300: 1,
    64: 2
}
SIZES = list(SIZES_MAP.keys())

if len(sys.argv) == 2:
    SIZE = int(sys.argv[1])
else:
    print(f"please provide a size \nHINT: size can be one of {SIZES}")
    sys.exit()


def display_image(image):
    width, height = image.size
    ascii_image = []
    for y in range(height):
        line = []
        for x in range(width):
            pixel = image.getpixel((x, y))
            term_pixel = f"\033[38;2;{pixel[0]};{pixel[1]};{pixel[2]}m{CHAR}\033[0m"
            line.append(term_pixel)
        ascii_image.append("".join(line))

    for line in ascii_image:
        print(line)


if __name__ == "__main__":
    if SIZE in SIZES:
        currSong = Spotify.current_user_playing_track()
        currSong = json.dumps(currSong)
        currSong = json.loads(currSong)

        if currSong is not None:
            coverURL = currSong["item"]["album"]["images"][SIZES_MAP[SIZE]]["url"]
            image = urllib.request.urlretrieve(coverURL, "cover.png")

            image = PIL.Image.open("cover.png")
            display_image(image)
        else:
            print("no playback")
            sys.exit()

    else:
        print(f"size can only be one of {SIZES}")
        sys.exit()
