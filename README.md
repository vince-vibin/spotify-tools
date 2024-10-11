# spotify-tools
A collection of commandline tools to better your spotify expirience using the spotify api

## artists

### [create artist mix](artists/create_artist_mix.py)
Here you can create a mix for an artist. This could be usefull if you want to donwload all the songs of one artist.  
`usage: create artist mix [-h] [--name NAME] [--size SIZE] [--mode MODE] artist_link`


## images

### [cli cover](images/cli_cover.py)
A script to output the cover of the song you are currently listening to to the cli as ascii art. This could be usefull if you want to use it in something like neofetch.

## converting
### [convert2gta.py](converting/convert2gta.py)
Here you can download Spotify Playlists to then use them in GTA V Self Radio. Songs are downloaded from YouTube and then moved to the GTA Music Folder.  
`usage: import to gta v [-h] playlist_link gta_musicfolder`


# Script Ideas
- [x] Album Cover Poster Generator
- [x] Convert Spotify Playlist to GTA V Radio
- [x] Convert Spotify Playlist to MP3
- [ ] Convert Spotify Playlist to Soundcloud (API currently not usable)
- [ ] Convert Spotify Playlist to Youtube Playlist (Costs money :/)
