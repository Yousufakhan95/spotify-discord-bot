import discord
import json
from spotify_client import SpotifyAPI
import time

#data
with open('creds.json') as cred_data:
  data = json.load(cred_data)

user_id = ""# please enter user id here

#setting up 
spot = SpotifyAPI(
    client_id = data['spotify_data']['spotify_client_id'],
    client_secret = data['spotify_data']['spotify_client_secret'],
    redirect_uri= 'https://www.google.com'
    )

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    current_user = client.user
    if message.author == current_user:
        return current_user

    #makes playlists
    if message.content.startswith('^mp'):
        # user adds playlist name after the call string
        playlist_name = message.content.replace('^mp ', '')
        # template == make_playlist(self, user_id, name, description)
        spot.make_playlist(user_id = user_id, name= playlist_name, description = 'this playlist was created by vinly')
        # gives message to user that there message is being created
        await message.channel.send(f'Playlist is being created, please wait.')
        # waits 5 seconds to get url cause lag
        time.sleep(5)
        #gets playlist_url
        playlist_url = spot.get_playlist_url(user_id = user_id, playlist_name = playlist_name)
        # need to return playlist url with it
        await message.channel.send(f'Playlist has been\n{playlist_url}')

    #add track to given playlist
    elif message.content.startswith('^ap'):
        # user adds track name after the call string
        #template
        # vinyl add track to playlist (song_name)@(playlist_url)
        track_name_and_playlist_url = message.content.replace('^ap ', '')
        for count,char in enumerate(track_name_and_playlist_url):
            if char == '@':
                track_name = track_name_and_playlist_url[:count]
                playlist_url = track_name_and_playlist_url[count+1:]

        try:
            # template == searched_track_to_add(self, query, search_type, playlist_url)
            spot.searched_track_to_add(query = track_name, search_type = 'track', playlist_url = playlist_url)
            await message.channel.send(f'{track_name} has been added to the provided playlist! here! \n{playlist_url}')
        except:
            await message.channel.send('invalid track name or playlist url')

    elif message.content.startswith('^vinylhelp'):
        # sends bot commands
        await message.channel.send('To create a playlist, use the following command `^mp (playlist_name)`\nTo add tracks to an existing playlist, use the following command `^ap (track_name@playlist_url)`')

    #ideas for bots
    

client.run(data['discord_token'])