import requests
import re
import os

def get_songs(search_term):
    response = requests.get("https://pagalnew.com/search.php?find=" + search_term)
    songs = re.findall(r'<a href="(/songs/[^"]+)">([^"]+)</a>', response.text)
    return songs

def get_albums(search_term):
    response = requests.get("https://pagalnew.com/search.php?find=" + search_term)
    albums = re.findall(r'<a href="(/album/[^"]+)">([^"]+)</a>', response.text)
    return albums

def download_song(song_url):
    song_name = song_url.split("/")[-1]
    response = requests.get(song_url)
    with open(song_name, "wb") as f:
        f.write(response.content)

def download_album(album_url):
    songs = get_songs(album_url)
    for song in songs:
        download_song(song)

def main():
    search_term = input("Enter a search term: ")
    print()

    if search_term == "":
        print("Please enter a search term.")
        return

    type = input("Do you want to download a song (s) or an album (a)? ")
    print()

    if type not in ["s", "a"]:
        print("Invalid type.")
        return

    if type == "s":
        songs = get_songs(search_term)
        if len(songs) == 0:
            print("No songs found.")
            return

        print("Here are the songs that were found:")
        for i, song in enumerate(songs):
            print(f"{i + 1}. {song[1]}")

        song_number = int(input("Enter the number of the song you want to download: "))
        print()

        if song_number > len(songs):
            print("Invalid song number.")
            return

        download_song(songs[song_number - 1][0])

    elif type == "a":
        albums = get_albums(search_term)
        if len(albums) == 0:
            print("No albums found.")
            return

        print("Here are the albums that were found:")
        for i, album in enumerate(albums):
            print(f"{i + 1}. {album[1]}")

        album_number = int(input("Enter the number of the album you want to download: "))
        print()

        if album_number > len(albums):
            print("Invalid album number.")
            return

        download_album(albums[album_number - 1][0])

if __name__ == "__main__":
    main()

