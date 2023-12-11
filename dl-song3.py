import re
import requests as req
import argparse
from urllib.parse import quote
from termcolor import colored
from bs4 import BeautifulSoup
from tqdm import tqdm

def die(e):
    print(colored("ERROR: "+e, "red"))
    exit(1)

def warn(e):
    print(colored("WARN: "+e, "yellow"))

def info(i):
    print(colored("INFO: "+i, "green"))

def help():
    print('''USES: dl-song.sh <argument> <song/album/movie name>
    arguments:
        -s or --song: to download a song
        -a or --album: to download all songs of a movie
    ''')

def dl_song(name:str):
    info("Downloading a song")
    res = req.get("https://pagalnew.com/search.php?find="+quote(name))
    #soup = BeautifulSoup(res.text, "html.parser")
    #anchor_tags = soup.find_all("a")
    song_urls = re.findall(r'/songs/[a-zA-Z0-9_-]*', res.text)
    if len(song_urls) == 0:
        die("No song found!!")
    for i,s in enumerate(song_urls):
        print(f"\t{i+1}."+s.split('/')[2].split('.')[0])
    selected_song_index = int(input("Enter a number:")) - 1
    print("You have selected "+'"'+song_urls[selected_song_index].split('/')[2].split('.')[0]+'"')
    selected_song_url = "https://pagalnew.com"+song_urls[selected_song_index]+".html"
    print(selected_song_url)
    res = req.get(selected_song_url)
    dl_link = "https://pagalnew.com"+re.findall(r'/download320/[0-9]*', res.text)[0]
    res = req.get(dl_link, stream=True)
    total_size = int(res.headers.get('Content-Length'))
    progress_bar = tqdm(total=total_size, desc=colored("Downloading...",'green'))
    with open("out.mp3", "wb") as f:
        for chunk in res.iter_content(chunk_size=1024):
            f.write(chunk)
            progress_bar.update(len(chunk))

def dl_album(name:str):
    #die("NOT IMPLEMENTED")
    info("Downloading a album")
    res = req.get("https://pagalnew.com/search.php?find="+quote(name))
    album_urls = re.findall(r'/album/[a-zA-Z0-9_-]*', res.text)
    print(res.text)
    print(album_urls)
    for i in range(len(album_urls)):
        print(f"{i}. {album_urls[i]}")
    index = int(input("Enter the album: "))
    dl_url = album_urls[index] + '.html'
    res = req.get("https://pagalnew.com"+dl_url)
    song_urls = re.findall(r'/songs/[a-zA-Z0-9_-]*', res.text)
    for url in song_urls:
        selected_song_url = "https://pagalnew.com"+url+".html"
        print(selected_song_url)
        res = req.get(selected_song_url)
        dl_link = "https://pagalnew.com"+re.findall(r'/download320/[0-9]*', res.text)[0]
        res = req.get(dl_link, stream=True)
        total_size = int(res.headers.get('Content-Length'))
        progress_bar = tqdm(total=total_size, desc=colored("Downloading...",'green'))
        with open(url.split("/")[2], "wb") as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)
                progress_bar.update(len(chunk))

def start():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--album', action='store_true')
    parser.add_argument('-s', '--song', action='store_true')
    parser.add_argument('-n', '--name', action='store')
    args = parser.parse_args()
    print(args)
    print("program is started")
    if (args.album and args.song):
        help()
        die("You can't select both album and song")
    elif (args.album):
        print("you have selected album")
        if (args.name == None):
            die("You have to enter the name of a song")
        dl_album(args.name)
    elif (args.song):
        print("you have selected song")
        if (args.name == None):
            die("You have to enter the name of a song")
        dl_song(args.name)
    else:
        help()
        die("You must select either album or song")

start()
