#!/usr/bin/env python3
import playsound
import configparser
import asyncio
import time
import random
import spotipy
import webbrowser
from spotipy.oauth2 import SpotifyClientCredentials
from pywizlight import wizlight, PilotBuilder, discovery

red = 128
green = 128
blue = 64
cycletime = 60
flash_variance = 25
how_chill = 220
scope = "ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming"
playlist = "spotify:playlist:37i9dQZF1EIe80k6uRBZGd"
sound_effect = "chill.wav"
config = configparser.ConfigParser()
config.read(".spotify.ini")
username = config["DEFAULT"]["username"]
spotify_id = config["DEFAULT"]["client_id"]
spotify_secret = config["DEFAULT"]["client_secret"]
redirectURI = config["DEFAULT"]["redirectURI"]
oauth_object = spotipy.SpotifyOAuth(
    client_id=spotify_id,
    client_secret=spotify_secret,
    redirect_uri=redirectURI,
    scope=scope,
)
token_dict = oauth_object.get_access_token()
token = token_dict["access_token"]
spotify = spotipy.Spotify(auth=token)
spotify.start_playback(context_uri=playlist)

# wiz bulb configuration
config = configparser.ConfigParser()
config.read(".wizbulb.ini")
backdrop_bulbs = config["DEFAULT"]["backdrop_bulbs"].split(" ")
overhead_bulbs = config["DEFAULT"]["overhead_bulbs"].split(" ")
battlefield_bulbs = config["DEFAULT"]["battlefield_bulbs"].split(" ")

world_bulbs = backdrop_bulbs + overhead_bulbs + battlefield_bulbs
light_bulbs = []
for b in world_bulbs:
    bulb = wizlight(b)
    light_bulbs.append(bulb)


async def main():
    try:
        playsound.playsound(sound_effect, True)
    except:
        print(f"likely need to make {sound_effect}")
    for light_bulb in light_bulbs:
        dim = how_chill - int(random.random() * 120)
        delta1 = int(random.random() * 20)
        delta2 = int(random.random() * 20)
        await light_bulb.turn_on(
            PilotBuilder(
                rgb=(red + delta1, green + delta2, blue + delta1), brightness=dim
            )
        )
    while True:
        print("start")
        random.shuffle(light_bulbs)
        # Pulse the light bulbs red
        for light_bulb in light_bulbs:
            if int(random.random() * 100) > 95:
                print("flash")
                flash_bright = how_chill - int(random.random() * flash_variance)
                await light_bulb.turn_on(
                    PilotBuilder(rgb=(255, 255, 255), brightness=flash_bright)
                )
                time.sleep(1)
            dim = how_chill - int(random.random() * 181)
            delta1 = int(random.random() * 20)
            delta2 = int(random.random() * 20)
            await light_bulb.turn_on(
                PilotBuilder(
                    rgb=(red + delta1, green + delta2, blue + delta1), brightness=dim
                )
            )
            time.sleep(cycletime / len(light_bulbs))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
