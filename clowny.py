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

green = 15
blue = 15
cycletime = 12
flash_variance = 25
scope = "ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming"
playlist = "spotify:playlist:1gauLmjFqDP3iP7yKiJCHt"
sound_effect = "dooropen.wav"
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

# wiz bulb configuration
config = configparser.ConfigParser()
config.read(".wizbulb.ini")
backdrop_bulbs = config["DEFAULT"]["backdrop_bulbs"].split(" ")
overhead_bulbs = config["DEFAULT"]["overhead_bulbs"].split(" ")
battlefield_bulbs = config["DEFAULT"]["battlefield_bulbs"].split(" ")

torch_scenes = [4]

backdrop_bulb_objs = []
for b in backdrop_bulbs:
    bulb = wizlight(b)
    backdrop_bulb_objs.append(bulb)

overhead_bulb_objs = []
for b in (overhead_bulbs + battlefield_bulbs):
    bulb = wizlight(b)
    overhead_bulb_objs.append(bulb)


async def main():
    try:
        playsound.playsound(sound_effect, True)
    except:
        print(f"likely need to make {sound_effect}")
    spotify.start_playback(context_uri=playlist)
    for light_bulb in backdrop_bulb_objs + overhead_bulb_objs:
        dim = 255 - int(random.random() * 60)
        speed = 10 + int(random.random() * 180)
        scene = random.choice(torch_scenes)
        await light_bulb.turn_on(PilotBuilder(scene=scene, speed=speed, brightness=dim))
    while True:
        print("start")
        random.shuffle(backdrop_bulb_objs)
        for light_bulb in backdrop_bulb_objs + overhead_bulb_objs:
            dim = 255 - int(random.random() * 60)
            speed = 10 + int(random.random() * 180)
            scene = random.choice(torch_scenes)
            await light_bulb.turn_on(
                PilotBuilder(scene=scene, speed=speed, brightness=dim)
            )
            time.sleep(cycletime / len(overhead_bulb_objs))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
