import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import util
import sys
import webbrowser
import time
import unidecode
import unicodedata

################################################################################
############################## CLASSES #########################################
################################################################################

class Argument:

    def __init__(self):
        self.verbose = False
        self.passive = False

################################################################################
############################## VARIABLES #######################################
################################################################################

# The username of the current user
username = ""

# To have the permission to get the current playing song (not the only possible
# option, see doc for more info: https://spotipy.readthedocs.io/en/2.7.0/)
scope = "user-read-currently-playing"

# The ID of the bot used
id = "55008f801dfc4da5b5f264b7e4833e80"

# The secret ID of the bot used
secret = "57b4a1608585428d919ddc8a6198c44d"

# My localhost, this could be an issue on your machine, make sure to set a localhost
# You can use Apache for example, more info: https://vitux.com/how-to-install-and-configure-apache-web-server-on-ubuntu/
url = "http://10.161.174.26/"

# Setting up the credentials, probably useless actually
ccm = SpotifyClientCredentials(client_id=id, client_secret=secret)

# Getting a token corresponding the user and the bot
token = util.prompt_for_user_token(username, scope, client_id=id, client_secret=secret, redirect_uri=url)

# The spotify object
spotify = spotipy.Spotify(auth=token, client_credentials_manager=ccm)

# Argument object
arguments = Argument()

# Feat token, this is what is used on Spotify most of the time to state a featuring
featToken = " (feat."

################################################################################
############################## METHODS #########################################
################################################################################

# Parse the arguments give as parameters
def parseArgs(arguments, argv):
    length = len(argv)

    # Parse all args
    for index in range(length):

        # If option -v has been passed, set verbose to True
        if argv[index] == "-v":
            arguments.verbose = True

        # If option -p is passe, set pasisve to True
        # If passive is set to True, new tabs will be opened each time a new song starts
        if argv[index] == '-p':
            arguments.passive = True

# Returns a string corresponding to the name of the band or artist as displayed
# on Spotify
# currentTrack should be a dictionnary you fetched with spotify.currently_playing()
# More info on the doc: https://spotipy.readthedocs.io/en/2.7.0/
def getBand(currentTrack):
    return currentTrack['item']['album']['artists'][0]['name']

# Returns a string corresponding to the name of the song as displayed on Spotify
# currentTrack should be a dictionnary you fetched with spotify.currently_playing()
# More info on the doc: https://spotipy.readthedocs.io/en/2.7.0/
def getSong(currentTrack):
    return currentTrack['item']['name']

# Returns a string corresponding to the name of the album as displayed on Spotify
# currentTrack should be a dictionnary you fetched with spotify.currently_playing()
# More info on the doc: https://spotipy.readthedocs.io/en/2.7.0/
def getAlbum(currentTrack):
    return currentTrack['item']['album']['name']

# Returns an easy to handle dictionnary that contains for fields:
# artist/band: The name of the artist or band as displayed on Spotify
# song: The name of the song as displayed on Spotify
# album: The namd of the album as displayed on Spotify
# These information correspond to the current song played, if none is being
# played or somethign went wrong, the dictionnary will be set to None
def getCurrentTrackAsDict(spotify):
    dict = {}

    try:
        currentTrack = spotify.currently_playing()
        dict['artist'] = getBand(currentTrack)
        dict['song'] = getSong(currentTrack)
        dict['album'] = getAlbum(currentTrack)
        dict['band'] = getBand(currentTrack)
    except Exception as e:
        print("No song is playing. Please make sure: ")
        print("         - Private Session is not enabled")
        print("         - Your username is correct")
        print("         - Spotify object has been correctly initialized")
        print("Detailed Error: ")
        print(e)
        dict = None

    return dict

# Displays the info stored in the track variable, assuming it was the variable
# returned by a call to getCurrentTrackAsDict
def displayTrackInfo(track):
    print("Artist/Band: " + str(track['band']))
    print("Song Name: " + str(track['song']))
    print("Album: " + str(track['album']))

# Spaces in Genius are transformed in dashes
def isSpace(c):
    return c == ' '

# Check if the character is a number, if it is it won't be modified
def isNumber(c):
    if c >= '0' and c <= '9':
        return True
    return False

# Check if the character is an upper case letter, if it is it won't be modified
# The thing is, with Genius URLs is that upper case letters do not matter
def isUpperCaseLetter(c):
    if c >= 'A' and c <= 'Z':
        return True
    return False

# Check if the character is an lower case letter, if it is it won't be modified
def isLowerCaseLetter(c):
    if c >= 'a' and c <= 'z':
        return True
    return False

# & is transformed in and in the language of the name of the song.
# Only english is handled for now, which is a major issue
# This will be especially hard to improve, so assume it will never end up working
def isSpecialAnd(c):
    return c == '&'

# Dashes are used in Spotify when there was an edit or a featuring etc. Often
# means the whole song name has been fetched
# That being said, it may not be the case, sometimes some dashes are in the name
# of the song, this is handled somewhere else
def isDash(c):
    return c == '-'

# This one is a funny one. Some song have interesting names to say the least.
# Had to take care of those I know, but this is surely not enough.
# If you ever encounter one of these songs, please send me a message and/or
# raise an issue on my GitHub
def isVerySpecial(c):
    if c >= '²' and c <= 'º' or c == 'ª':
        return True
    return False

# A feat, in Spotify, almost always starts with (feat. <name>)
# So that's how I get this here, by checking if this appears
# Of course there will be exceptions, please raise these as issues on my GitHub
def getIndexFeat(string):
    for index in range(len(string) - len(featToken)):
        if string[index:(index + len(featToken))] == featToken:
            return index
    return -1

# This locates the last dash (if any) used in the song title
# The part after the dash is generally (note that it's probably not always true)
# some meta information, such as "radio edit" which we don't want to use in the URL
# That being said, some song might be exceptions 
# If you ever encounter one of these songs, please send me a message and/or
# raise an issue on my GitHub
def lastDashIndex(string):
    for index in range(len(string)):
        if string[index:(index + 3)] == " - ":
            return index
    return -1

# Shamelessly copied from Stack Overflow 
# https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
# Works well enough to remove accents and weird stuff you can find on letters
# There could be some characters not correctly handled
# If you ever encounter one of these songs, please send me a message and/or
# raise an issue on my GitHub
def stripAccents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

# Format a string as genius format song and band names
# Most of the time it is straight forward:
# https://www.genius.com/band-song-lyrics.com
# If there are spaces in the band/song's name, these are replaced
# with dashes
# There are plenty of other little things they do so that the URL is standardized
# I try to take care of most of these things but I don't know every song in existence 
# So please inform me as soon as you find exceptions
# 
# Also, note that not any song has a Genius webpage. One way to handle that could 
# be to look on different sites but this is not a priority
def geniusFormat(string):

    # The final URL will be stored here
    newString = ""

    # Remove any Featuring there could be
    indexOfFeat = getIndexFeat(string)
    if indexOfFeat != -1:
        string = string[0:indexOfFeat]

    # Remove any meta information there could be
    indexOfLastDash = lastDashIndex(string)
    if indexOfLastDash != -1:
        string = string[0:indexOfLastDash]

    # Remove all accents and weird things on letters in general
    string = stripAccents(string)

    # Actual generation of the URL
    for index in range(len(string)):
        # Normal characters + dashes -> Do nothing, just add the caracter
        if isNumber(string[index]) or isLowerCaseLetter(string[index]) or isDash(string[index]):
            newString += string[index]

        # Upper case characters -> Lowercase the characters (it doesn't really matter though)
        if isUpperCaseLetter(string[index]):
            newString += string[index].lower()

        # Spaces -> Make them dashes
        if isSpace(string[index]):
            newString += '-'
        
        # & -> Make them "and"s. This is very bad, for there are other languages that exist
        if isSpecialAnd(string[index]):
            newString += "and"

        # Weird characters I happened to find in different songs (see above)
        # Just, make them unicode and add them
        if isVerySpecial(string[index]):
            newString += unidecode.unidecode(string[index])

    return newString

# Returns a URL hopefully leading to the current playing song
# If the song doesn't have a Genius page it will obviously not open a valid
# page. As I said above, this can be taken care of by using different sites
def createGeniusUrlFromTrack(track):
    url = "https://www.genius.com/"
    url += geniusFormat(track['band'])
    url += "-"
    url += geniusFormat(track['song'])
    url += "-lyrics"
    return url

# Opens the tab in an availible web browser or opens a new one
def openTab(spotify, arguments):
    # Get the track's info
    track = getCurrentTrackAsDict(spotify)

    # Gets the Genius URL
    geniusUrl = createGeniusUrlFromTrack(track)

    # Display track infos if required
    if arguments.verbose:
        displayTrackInfo(track)
        print(geniusUrl)

    # Opens the Genius URL hopefully
    webbrowser.open(geniusUrl)

# Opens the tab in an availible web browser or opens a new one
# Then wait for a new song to start to open a new tab with the new song's lyrics
def passiveOpenTab(spotify, arguments):

    # The URL of the last song a tab was opened for
    # Basically prevents the software to open a thousand million tabs in a second
    lastUrl = ""

    # As long as the user doesn't require the tab to be closed
    # Temporary, should change with the GUI
    while True:

        # Get the track's info
        track = getCurrentTrackAsDict(spotify)

        # Gets the Genius URL
        geniusUrl = createGeniusUrlFromTrack(track)

        # Display track infos if required
        if arguments.verbose:
            displayTrackInfo(track)
            print(geniusUrl)

        # If the song changed
        if lastUrl != geniusUrl:

            # Opens the Genius URL hopefully
            webbrowser.open(geniusUrl)

            # Sets the previous URL to be this one
            lastUrl = geniusUrl

        # Avoid setting to many requests to Spotify
        time.sleep(0.5)

################################################################################
############################## EXECUTION #######################################
################################################################################

# Read and interpret passed arguments
# As a reminder :
# -p : Passive listening (see below)
# -v : Verbose
parseArgs(arguments, sys.argv)

# If it should open new tabs each time a new song starts
# This is set with parameter -p
# Basically, this will open a new tab each time a new song starts, this is useful 
# if you want to listen to a lot of songs in a row
# Something pretty annoying though, is that as far as I know, it is not possible to close
# an opened tab
# This is possible with Selenium but Selenium opens a new internet browser, which I don't 
# really like
if arguments.passive:
    passiveOpenTab(spotify, arguments)
else:
    openTab(spotify, arguments)
