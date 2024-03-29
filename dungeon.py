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
cycletime = 2
flash_variance = 25
scope = "ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming"
playlist = "spotify:playlist:2q6tU7SrOYgtSPw2x1cGt0"
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

# wiz bulb configuration
config = configparser.ConfigParser()
config.read(".wizbulb.ini")
backdrop_bulbs = config["DEFAULT"]["backdrop_bulbs"].split(" ")
overhead_bulbs = config["DEFAULT"]["overhead_bulbs"].split(" ")
battlefield_bulbs = config["DEFAULT"]["battlefield_bulbs"].split(" ")

torch_scenes = [5, 28, 31]

backdrop_bulb_objs = []
for b in backdrop_bulbs:
    bulb = wizlight(b)
    backdrop_bulb_objs.append(bulb)

overhead_bulb_objs = []
for b in overhead_bulbs:
    bulb = wizlight(b)
    overhead_bulb_objs.append(bulb)

battlefield_bulb_objs = []
for b in battlefield_bulbs:
    bulb = wizlight(b)
    battlefield_bulb_objs.append(bulb)

world_bulbs = backdrop_bulb_objs + overhead_bulb_objs + battlefield_bulb_objs


async def main():
    spotify.start_playback(context_uri=playlist)
    try:
        playsound.playsound(sound_effect, False)
    except:
        print(f"likely need to make {sound_effect}")
    for light_bulb in backdrop_bulb_objs:
        dim = 128 - int(random.random() * 60)
        speed = 10 + int(random.random() * 180)
        scene = random.choice(torch_scenes)
        await light_bulb.turn_on(PilotBuilder(scene=scene, speed=speed, brightness=dim))
    for light_bulb in overhead_bulb_objs:
        dim = 64 + int(random.random() * 20)
        delta1 = int(random.random() * 30)
        delta2 = int(random.random() * 30)
        delta3 = int(random.random() * 30)
        await light_bulb.turn_on(
            PilotBuilder(rgb=(32 + delta1, 32 + delta2, 32 + delta3), brightness=dim)
        )
    while True:
        print("start")
        random.shuffle(world_bulbs)
        for light_bulb in world_bulbs:
            if light_bulb in backdrop_bulb_objs:
                dim = 128 - int(random.random() * 60)
                speed = 10 + int(random.random() * 180)
                scene = random.choice(torch_scenes)
                await light_bulb.turn_on(
                    PilotBuilder(scene=scene, speed=speed, brightness=dim)
                )
            else:
                dim = 32 + int(random.random() * 20)
                delta1 = int(random.random() * 30)
                delta2 = int(random.random() * 30)
                delta3 = int(random.random() * 30)
                await light_bulb.turn_on(
                    PilotBuilder(
                        rgb=(32 + delta1, 32 + delta2, 32 + delta3), brightness=dim
                    )
                )
            time.sleep(cycletime / len(world_bulbs))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
