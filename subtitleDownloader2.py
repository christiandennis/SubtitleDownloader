#!/usr/bin/env python
import os
import hashlib
import requests
import sys

list_of_subs = "http://api.thesubdb.com/?action=search&hash="
download_subs = "http://api.thesubdb.com/?action=download&hash="
headers = {"User-Agent" : "SubDB/1.0 (subsDown/0.1; http://theaidorus.github.io)"}
fileExtension = [".mkv", ".mp4", ".avi", ".3gp"]
depthLimit = 4

def get_hash(name):
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            size = os.path.getsize(name)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()


def scan(path, depth=0):
    if depthLimit and depth>=depthLimit:
        return

    try:
        for file in os.listdir(path):
            filename, ext  =  os.path.splitext(path+"/"+file)
            hashFile=0;
            if ext in fileExtension:
                hashFile = get_hash(path+"/"+file)
                respond = requests.get(list_of_subs+hashFile, headers=headers)
                subs = requests.get(download_subs+hashFile+"&language=en", headers=headers)
                if (subs.status_code==200):
                    f = open(filename+".srt", 'w')
                    f.write(subs.content)
                    f.close()

            if os.path.isdir(file):
                scan(path+"/"+file, depth+1)
    except:
        help()


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


if __name__ == "__main__":
    if len(sys.argv)==1:
        scan(os.getcwd())
    elif len(sys.argv)==2 and sys.argv[1]=="help":
        help()
    elif len(sys.argv)==2:
        try:
            depthLimit = int(sys.argv[1])
            scan(os.getcwd())
        except:
            depthLimit = None
            scan(sys.argv[1])
    elif len(sys.argv)==3:
        try:
            depthLimit = int(sys.argv[2])
            scan(sys.argv[1])
        except:
            help()


