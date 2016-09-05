#!/usr/bin/env python
import os
import hashlib
import requests
import sys
import json

lang = "en"
download_api = "http://api.thesubdb.com/?action=download&hash="
header = {
    "User-Agent": "SubDB/1.0 (SubtitleDownloader; http://christiandennis.net"}
fileExtensions = [".mkv", ".mp4", ".avi", ".3gp"]
depthLimit = 4


def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def scan(path, depth=0):
    if depthLimit and depth >= depthLimit:
        return

    data_f = None
    try:
        data_f = open(".subtitleDownloaderData", "r+")
    except:
        data_f = open(".subtitleDownloaderData", "w+")

    downloaded = {}
    try:
        downloaded = json.loads(data_f.read())
    except:
        downloaded = {}

    try:
        for filename in os.listdir(path):
            fullpath, ext = os.path.splitext(path+"/"+filename)
            if ext in fileExtensions:
                subs = requests.get(
                    download_api +
                    get_hash(path+"/"+filename) +
                    "&language=" + lang,
                    headers=header)
                if (subs.status_code == 200):
                    f = open(fullpath+".srt", 'w')
                    f.write(subs.content)
                    f.close()
                    print(lang + " subtitle for " + filename + " has been downloaded.")
            elif os.path.isdir(filename):
                if filename in downloaded:
                    continue
                downloaded[filename] = 0
                scan(path+"/"+filename, depth+1)
    except:
        help()

    data_f.seek(0)
    data_f.truncate()
    data_f.write(json.dumps(downloaded))
    data_f.close()


def help():
    print("SubtitleDownloader:")
    print("Easiest way to use: cd to desired parent directory and run 'sd'")
    print("USAGE:")
    print("1. 'sd'            : to download all movies' subtitles including subfolders")
    print("2. 'sd number'     : to download all movies' subtitles including subfolders. number is the subfolder depth limit")
    print("3. 'sd dir'        : to download all movies' subtitles including subfolders in dir")
    print("4. 'sd dir number' : to download all movies' subtitles including subfolders in dir. number is the subfolder depth limit")
    print("\ndir must be a valid directory")
    print("number must be integer. the default is set to 4")
    print("\nSubtitleDownloader will skip subfolder that SubtitleDownloader has downloaded its subtitle before. Edit/delete file '.subtitleDownloaderData' to modify the list of processed folder.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        scan(os.getcwd())
    elif len(sys.argv) == 2 and sys.argv[1] == "help":
        help()
    elif len(sys.argv) == 2:
        try:
            depthLimit = int(sys.argv[1])
            scan(os.getcwd())
        except:
            depthLimit = None
            scan(sys.argv[1])
    elif len(sys.argv) == 3:
        try:
            depthLimit = int(sys.argv[2])
            scan(sys.argv[1])
        except:
            help()
