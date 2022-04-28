# Program made by @Daniël.KvG
# This project will connect with spotify when active.
# When spotify is active, the code will scrape information about the song that is playing
# With the information gathered, the songs lyrics will be shown on a screen such that the relevant lyrics is always on screen.
# inspiration: https://www.youtube.com/watch?v=cU8YH2rhN6A&t=1557s

import spotipy as sp
import lyricsgenius as lg
from .myconfig import *

#CONNECT
#Spotify
SPOTIPY_REDIRECT_URI = "http://google.com"
SCOPE = "user-read-currently-playing"                           #define the scope of our request

spOauth = sp.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE) #insert data in the class SpotifyOAuth which will help to authenticate requests
token_dict = spOauth.get_cached_token()                   #use the authentication class to get a dictionary containing the access token
spotify_access_token = token_dict["access_token"]               #extract the access token from the dictionary

spotify_object = sp.Spotify(auth=spotify_access_token)          #initialize the spotify object

#Genius
genius_object = lg.Genius(genius_access_token)                  #initialize the lyricsgenius object

#SCRAPE INFO
playing = spotify_object.currently_playing()                    #scrape all information about the song that is playing

class Getters:
    oauth_object = spOauth
    token_dict = oauth_object.get_cached_token()                   #use the authentication class to get a dictionary containing the access token
    spotify_access_token = token_dict["access_token"]               #extract the access token from the dictionary

    spotify_object = sp.Spotify(auth=spotify_access_token)          #initialize the spotify object

    playing = spotify_object.currently_playing()                    #get a dictionary about the song that is

    def __init__(self) -> None:
        pass

    def Refresh(self):
        g.playing = g.spotify_object.currently_playing()                    #scrape all information about the song that is playing

        if g.oauth_object.is_token_expired(g.token_dict) == True:
            g.oauth_object = sp.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE)

        if g.playing == None:
            print("refreshing")
            token_dict = g.oauth_object.get_cached_token()                   #use the authentication class to get a dictionary containing the access token
            spotify_access_token = token_dict["access_token"]               #extract the access token from the dictionary
            g.spotify_object = sp.Spotify(auth=spotify_access_token)          #initialize the spotify object

        return g.playing


    def GetLength(self):
        try:
            playing = Getters.Refresh(self)
            length = playing['item']['duration_ms']                         #song length
            print("length is:", (length/60000))
        except:
            length = "0"
        return length

    def GetProgress(self):        
        try:
            playing = Getters.Refresh(self)
            progress = playing['progress_ms']                               #song progress
        except:
            progress = "0"
        return progress

    def GetLyrics(self):
        try:
            playing = Getters.Refresh(self)
            #print(json.dumps(playing, sort_keys=False, indent=4))         #use json.dumps for pretty printing
            artist_name = playing["item"]["album"]['artists'][0]['name']    #get the artist name by searching the keys in the nested dictionary stored in the variable playing
            song_title = playing['item']['name']                            #song name
            
            #LYRICS
            #look for available lyrics (Genius)
            song = genius_object.search_song(title=song_title, artist=artist_name)  #find the song on lyricsgenius
            try:
                lyrics = song.lyrics                                                   #get the lyrics
                format_lyrics = lyrics.replace('\n', '<br>')
                print('lyrics found')

            except:
                format_lyrics = "No lyrics available for this song."
                print('error: lyrics not found')

        except:
            format_lyrics = "Play a song"
    
        return format_lyrics

#define class and run all functions for the first time loading
g = Getters()
g.GetLength()
g.GetProgress()
g.GetLyrics()


# def PrintLyrics():
#     while True:
#         try:        
#             if result == GetLyrics():
#                 time.sleep(3)
#             else:
#                 result = GetLyrics()
#                 print(result)
#         except:
#             print("ERROR: printlyrics")
#             time.sleep(3)