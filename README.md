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

[Set up an Apache account](https://vitux.com/how-to-install-and-configure-apache-web-server-on-ubuntu/).
Then you may need to change the url variable line in the VARIABLES section.

### Something else?

Raise an issue or contact me, or both.

## Known Issues

### The generated URL is incorrect

There are a lot of cases to handle and it is not possible to fidn them all alone. Thankfully you can help! Just contact me or raise an issue, or both.

### The generated URL is incorrect and contains this symbol : "&"

If the name of the sond is not english, this is expected behaviour, unfortunately. For now, different languages are not handled because this is far from easy. I am opened to suggestions of course.

### The generated URL seems correct but not lyrics are displayed

Genius do not have every lyrics of every song to exist, unfortunately. You can write the lyrics by yourself, if you want, then it should work. This may be handled in future releases though.

## Copyright

© 2020 Spotify AB

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

If you modify this work, please see [this page](https://developer.spotify.com/terms/) for more legal information.