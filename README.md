# Spotify-Lyrics

This python script will (hopefully) allow users to have lyrics being displayed when they use Spotify. The way it works is that it opens a tab in an active webbrowser (or open one then open a tab). In this tab you can find the lyrics of the current song you are listening on Spotify.

## Installation

For now you just download the script and run it on your computer. I might give an installation file someday, to add it at least on Linux. But not very likely.

## Usage

There are 2 availible modes.

### For one song only

```bash
python Spotify-Lyrics.py
```

This will open the new tab with the lyrics of the current playing songs on Spotify and stop the software.

### Passive mode

```bash
python Spotify-Lyrics.py -p
```

This will open the new tab with the lyrics of the current playing songs on Spotify. Then it will wait until a new song starts to repeat the process.

## Troubleshooting

### I get errors, what should I do?

Normally, the error message states anything that could have gone wrong. Just in case, if you missed it, this software doesn't work if you are in a Private Session. Also, you might have entered an incorrect username. If both of these things didn't work, please raise an issue.

### It opens a weird Ubuntu tab, what should I do?

Copy the URL and paste it in the terminal, it should be fine.

### I get errors about redirect_url, what should I do?

[Set up an Apache account](https://vitux.com/how-to-install-and-configure-apache-web-server-on-ubuntu/)
Then you may need to change the url variable line in the VARIABLES section.

### Something else?

Raise an issue or contact me, or both.