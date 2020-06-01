import os
from os.path import join
import subprocess
from pytube import Playlist, YouTube  # pip install pytube3
from glob import glob
import moviepy.editor as mp  # pip intall moviepy
from time import sleep


def get_audio_from_youtube_playlist(playlist, output_path=r"c:/tmp"):
    # converts the link to a YouTube object
    # playlist.remove('https://www.youtube.com/watch?v=0SLCpL1lGDc')
    for i, song in enumerate(playlist):
        print('{:.1f}% done: '.format(float(100*i)/float(len(playlist))) + song)
        # track = YouTube(song).streams.filter(only_audio=True).all()
        if not check_if_downloaded(output_path, song):
            try:
                default_filename, track = get_audio_track(song)
                print("Downloading " + default_filename + "...")
                track.download(output_path)
            except OSError:
                print("url error")
            else:
                add_to_saved_list(output_path, song)
    print("Download finished.")


def get_audio_track(song):
    try:
        track = YouTube(song).streams.get_audio_only()
    except KeyError:  # if at first you don't succeed, try, try again
        sleep(0.5)
        try:
            track = YouTube(song).streams.get_audio_only()
        except KeyError:  # one more time...
            sleep(0.5)
            track = YouTube(song).streams.get_audio_only()
    default_filename = track.default_filename
    if 'YouTube' in track.title:
        print('trying again')
        default_filename, track = get_audio_track(song)
    return default_filename, track


def convert_mp4_to_mp3_using_subprocess(default_filename, output_path):
    # converts mp4 audio to mp3 audio
    print("Converting to mp3....")
    new_filename = default_filename[0:-3] + "mp3"
    os.rename(os.path.join(output_path, default_filename), os.path.join(output_path, 'tmp.mp4'))
    subprocess.run(['ffmpeg', '-i', os.path.join(output_path, 'tmp.mp4'), os.path.join(output_path, 'tmp.mp3')])
    os.remove(os.path.join(output_path, 'tmp.mp4'))
    os.rename(os.path.join(output_path, 'tmp.mp3'), os.path.join(output_path, new_filename))


def convert_mp4_to_mp3(tgt_folder):
    files = glob(tgt_folder + r'/*.mp4')
    for file in files:
        audio_file = mp.AudioFileClip(file)  # .subclip(10, )  # disable if do not want any clipping
        audio_file.write_audiofile(file[:-4]+'.mp3')
        try:
            os.remove(file)
        except PermissionError:
            print("could not delete file because it is being used by another process")


def download_youtube_playlist_to_mp3(playlist_html, download_path=r'c:/tmp', convert_to_mp3=True):
    if not os.path.isdir(download_path):
        os.mkdir(path=download_path)
    youtube_playlist = Playlist(playlist_html)
    get_audio_from_youtube_playlist(youtube_playlist, download_path)
    if convert_to_mp3:
        convert_mp4_to_mp3(download_path)
    print('file saved to {}'.format(download_path))


def download_youtube_link_to_mp3(yt_html, download_path=r'c:/tmp', convert_to_mp3=True):
    if not os.path.isdir(download_path):
        os.mkdir(path=download_path)
    default_filename, track = get_audio_track(yt_html)

    print("Downloading " + default_filename + "...")
    track.download(download_path)
    if convert_to_mp3:
        convert_mp4_to_mp3(download_path)
    print('file saved to {}'.format(download_path))


def add_to_saved_list(path, file_link):
    try:
        with open(join(path, 'saved.txt'), 'a') as f:
            f.write("%s\n" % file_link)
    except FileNotFoundError:
        with open(join(path, 'saved.txt'), 'w+') as f:
            f.write("%s\n" % file_link)


def check_if_downloaded(path, file):
    try:
        with open(join(path, 'saved.txt'), 'r') as f:
            downloaded_list = f.read()
            a = file in downloaded_list
    except FileNotFoundError:
        a = False
    return a


if __name__ == "__main__":
    download_destination = "C:/Users/eshwartz/Music/Howlin' Wolf Meets Muddy Waters"
    youtube_path = 'https://www.youtube.com/playlist?list=OLAK5uy_nvyNn18gQisV0TY4-fh1Kt3A6Zo08-RcI'
    if str(youtube_path).find('playlist') != -1:
        download_youtube_playlist_to_mp3(youtube_path, download_destination, convert_to_mp3=True)
    else:
        download_youtube_link_to_mp3(youtube_path, download_destination)
