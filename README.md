# Web Radio to Spotify

[![CircleCI](https://circleci.com/gh/ericdaat/webradio-to-spotify.svg?style=svg)](https://circleci.com/gh/ericdaat/webradio-to-spotify)

As a big fan of Classic Rock living in France, I am very frustrated by the
lack of good classic rock radio we have. I spent four months in St Louis, MO,
and I had the chance to listen to [KSHE 95](http://www.kshe95.com/) every day,
playing some of my favorite classic rock tunes.
Unfortunately, I can't listen to this radio in France as they block it.
Fortunately, their website shows the tune currently playing, as well
as a few previous ones.

I decided to make myself an empty
[Spotify playlist](https://open.spotify.com/user/ericda/playlist/3BCcE8T945z1MnfPWkFsfX),
and automatically add in the KSHE tracks.
I also wanted to be able to add songs
from other similar Classic Rock radio. So I built a reusable architecture that
enables to register different web scrapers to get the radio playing history
and add that into my playlist.

So far, I am able to get the songs from these radios:

- [KSHE95 (St Louis, MO)](https://www.kshe95.com/)
- [The Eagle 969 (Sacramento, CA)](https://eagle969.radio.com/)

Feel free to ping me if you want to help!

## Installation

To make it work, here's what to do.

First, you'll need to setup your Spotify developer account, and register an app.
Find how [here](https://developer.spotify.com/web-api/).
Once your app is created, you will have access to the following crendentials:

- `client_id`
- `client_secret`
- `redirect_uri`

The app will need those to update tracks to your playlist.

Copy the file `.spotify-token.json.dist` into `.spotify-token.json`
and fill in these credentials. You will also need to add:

- Your spotify *user_id* (your username)
- The *playlist_id* to which you'll upload the tracks to
  (e.g mine is `3BCcE8T945z1MnfPWkFsfX`)

Once you're good, install the requirements in a virtual environment:

``` shell
pip install virtualenv  # if you don't have it already
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

The app uses an `sqlite` database to store all the songs it has downloaded so far. You have to initialize the database running this command: `make init-db`.

Here are the required steps to update your playlist with
the latest songs from the KSHE radio:

- First, launch the server: `make start-api`. The app should now be running on `http://localhost:9999`.
- Then, open your browser and go to `http://localhost:9999/auth` to authenticate to Spotify.
- Finally, run `make update-playlist` to get the latest songs in your playlist.

## API

The calls supported so far are:

- [GET] `localhost:9999/`: Check that the app is up
- [GET] `localhost:9999/auth`: Authenticate for 3600 seconds
- [POST] `localhost:9999/update_playlist`: Updates the playlist with the latest songs
