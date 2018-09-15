import requests
import string
import json
import re
import urllib.request
from bs4 import BeautifulSoup

def getArtistPage(artist):
    """ 
    This function requests the webpage and parses it with Beautiful
    Soup, returning the resulting Beautiful Soup object, soup. The 
    webpage is a list of the artist's top songs.
    """

    # Find the artist page's url on metrolyrics.com
    artist = artist.split(' ')
    artistToURL = artist[0]
    if len(artist)>1:
    	artistToURL += ('-'+artist[1])
    url = "http://www.metrolyrics.com/"+ artistToURL +"-lyrics.html"

    response = requests.get(url)   # request the page

    if response.status_code == 404:                 # page not found
        print("There was a problem with getting the page:")
        print(url)

    data_from_url = response.text                   # the HTML text from the page
    soup = BeautifulSoup(data_from_url,"lxml")      # parsed with Beautiful Soup
    return soup

def getLyricPage(artist, song):
    """ 
    This function requests the webpage and parses it with Beautiful
    Soup, returning the resulting Beautiful Soup object, soup. The 
    webpage is the song's lyrics.
    """

    # Find the lyric page url on metrolyrics.com
    artist = artist.split(' ')
    song = song.split(' ')
    
    artistToURL = artist[0]
    songToURL = song[0]
    
    if len(song)>1:
    	for i in range(1, len(song)):
    		songToURL += ('-'+song[i])
    if len(artist)>1:
    	for i in range(1, len(artist)):
    		artistToURL += ('-'+artist[i])	
    url = "http://www.metrolyrics.com/"+ songToURL + "-lyrics-" + artistToURL +".html"
    response = requests.get(url)   # request the page

    if response.status_code == 404:                 # page not found
        print("There was a problem with getting the page:")
        print(url)

    data_from_url = response.text                   # the HTML text from the page
    soup = BeautifulSoup(data_from_url,"lxml")      # parsed with Beautiful Soup
    return soup    


def extractSongs(artist):
	"""
	This function extracts the artist's top songs from the soup.
	The soup is scraped from the webpage containing the artist's top songs.
	The top songs are compiled into the list, topSongsList. 
	"""
	soup = getArtistPage(artist)
	# songList contains all text segments with the tag <a alt = ...>
	songList = soup.findAll('a', alt=True)
	topSongsList = []
	
	# Find the index of the element in songList that is the first top song.
	# We do this because metrolyrics lists the artist's latest releases first,
	# but we only want the artist's top songs.
	indexTopSongs = 0
	for i in range(len(songList)):
		songRaw = str(songList[i])
		# Once we find the index of the first top song, break out of the loop.
		if 'class="title hasvidtable"' in songRaw:
			indexTopSongs = i
			break
	
	# Compile a list of the artist's top 15 songs.
	for i in range(indexTopSongs, indexTopSongs+15):
		songRaw = str(songList[i])
		# Delete the characters that are not part of the top song titles.
		leftStr = '<a alt="' + artist + ' '
		left = songRaw.find(leftStr) + len(leftStr)
		rightStr = ' lyrics"'
		right = songRaw.find(rightStr)
		topSongsList.append(songRaw[left:right])
	return topSongsList

def extractLyrics(artist, song):	
	"""
	This function extracts the song lyrics from soup.
	The soup is scraped from the webpage containing the song's lyrics.
	The lyrics are returned as a string called wholeLyrics.
	"""
	soup = getLyricPage(artist, song)
	# lyricList contains all text segments with the tag <p class="verse"...
	lyricList = soup.findAll('p', {'class':'verse'})

	# Compile the verses of the song into the string wholeLyrics
	for i in range(len(lyricList)):
		lyricRaw = str(lyricList[i])
		# Delete the characters that are not part of the song's lyrics.
		left = lyricRaw.find('"verse">') + len('"verse">')
		right = lyricRaw.find('</p>')
		lyricList[i] = lyricRaw[left:right].replace('<br/>', '')
	wholeLyrics = ' '.join(lyricList)
	
	return wholeLyrics

def createDataset(artistList):
	"""
	Write the lyrics of the top songs from each artist in artistList to a text file.
	"""
	for artist in artistList:
		# Compile a list of the artist's top songs
		songList = extractSongs(artist)
		# Compile a text file of the lyrics from this artist
		file = open('lyricsdataset.txt', 'a')
		for song in songList:
			lyrics = extractLyrics(artist, song)
			print('-----------------------------', artist, '-', song)
			file.write(lyrics)

def main():
	# I created this artistList with my own knowledge of pop music. I figured these 
	# popular artists had lyrics that were simple enough for the RNN to replicate.
	artistList = ['Katy Perry', 'Ke$ha', 'Kelly Clarkson', 'Taylor Swift', 'Bruno Mars', 'Ariana Grande', 'Rihanna', 'Alicia Keys', 'Tinashe', 'SZA']
	createDataset(artistList)


if __name__ == "__main__":
	main()
