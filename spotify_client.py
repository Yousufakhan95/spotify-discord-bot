import spotipy

class SpotifyAPI(object):
    scope = ['playlist-modify-public','playlist-read-collaborative','playlist-modify-private', 'user-library-read']

    def __init__(self, client_id, client_secret, redirect_uri, *args, **kwargs):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        auth_manager = spotipy.SpotifyOAuth(
            client_id = self.client_id,
            client_secret = self.client_secret,
            redirect_uri = self.redirect_uri,
            scope = self.scope
        )
        self.spot_object = spotipy.Spotify(auth_manager=auth_manager)

    def search(self, query, search_type):
        response = self.spot_object.search(query, limit=1, offset=0, type=search_type, market=None)
        return {'track_link': response['tracks']['items'][0]['external_urls']['spotify'],
        'track_id': response['tracks']['items'][0]['id']}

    def make_playlist(self, user_id, name, description):
        #user_id is username if you dont have your facebook account linked.
        self.spot_object.user_playlist_create(user = user_id, name = name, public = True, collaborative= False, description = description)

    def add_track_to_given_playlist(self, items, playlist_url):
        #playlist url needs to be provieded
        #track url needs to be provided
        playlist_id = playlist_url.replace('https://open.spotify.com/playlist/', '')
        for index,chars in enumerate(playlist_id):
            if playlist_id[index] == '?' and playlist_id[index+1] == 's' and playlist_id[index+2] == 'i':
                playlist_id = playlist_id[:index]
                break
        self.spot_object.playlist_add_items(playlist_id = playlist_id, items = items, position = 0)

    def searched_track_to_add(self, query, search_type, playlist_url):
        track_data = self.search(query = query, search_type = search_type)
        self.add_track_to_given_playlist(items = [track_data['track_link']], playlist_url= playlist_url)

    def get_playlist_url(self, user_id, playlist_name):
        response = self.spot_object.user_playlists(user = user_id, limit=50, offset=0)
        if playlist_name == response['items'][0]['name']:
            link_dict = response['items'][0]['external_urls']
            return link_dict['spotify']