# SubtitleDownloader

inspired by https://github.com/theaidorus/SubtitleDownloader

SubtitleDownloader is a script to download english subtitles from video files within a folder and its subfolders.

SubtitleDownloader uses SubDB API http://thesubdb.com/api/


##Installation
###HomeBrew
```
brew tap christiandennis/cdennis
brew install sd
```
#####executable binary: dist/sd

##Usage
####Easy - recommended
run `sd` to download all movies' english subtitles in current working directory and its subfolders (4 levels deep)
####Not so easy
run `sd [number]` to download all movies' english subtitles in current working directory and its subfolders up to `number` depth.

run `sd [dir]` to download all movies' english subtitles in current working directory and its subfolders the given `dir`.

run `sd [dir] [number]` to download all movies' english subtitles in current working directory and its subfolders the given `dir` up to `number` depth.

run `sd help` for complete instructions.
#####Supports mp4, avi, mkv
