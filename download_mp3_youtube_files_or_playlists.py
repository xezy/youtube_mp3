import os
import subprocess
from numpy import logical_and
from pytube import Playlist, YouTube
from glob import glob


def get_audio_from_youtube_playlist(playlist, output_path=r"c:/tmp"):
    # converts the link to a YouTube object
    # playlist.remove('https://www.youtube.com/watch?v=0SLCpL1lGDc')
    for i, song in enumerate(playlist):
        print('{:.1f}% done: '.format(float(100*i)/float(len(playlist))) + song)
        # track = YouTube(song).streams.filter(only_audio=True).all()
        track = YouTube(song).streams.get_audio_only()
        default_filename = track.default_filename
        if logical_and(not os.path.isfile(os.path.join(output_path, default_filename[:-3] + 'mp3')),
                       not os.path.isfile(os.path.join(output_path, default_filename[:-3] + 'mp4'))):
            print("Downloading " + default_filename + "...")
            try:
                track.download(output_path)
            except OSError:
                print("url error")
    print("Download finished.")


def convert_mp4_to_mp3_using_subprocess(default_filename, output_path):
    # converts mp4 audio to mp3 audio
    print("Converting to mp3....")
    new_filename = default_filename[0:-3] + "mp3"
    os.rename(os.path.join(output_path, default_filename), os.path.join(output_path, 'tmp.mp4'))
    subprocess.run(['ffmpeg', '-i', os.path.join(output_path, 'tmp.mp4'), os.path.join(output_path, 'tmp.mp3')])
    os.remove(os.path.join(output_path, 'tmp.mp4'))
    os.rename(os.path.join(output_path, 'tmp.mp3'), os.path.join(output_path, new_filename))


def convert_mp4_to_mp3(tgt_folder):
    import moviepy.editor as mp
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
    print(yt_html)
    # track = YouTube(song).streams.filter(only_audio=True).all()
    track = YouTube(yt_html).streams.get_audio_only()
    default_filename = track.default_filename
    print("Downloading " + default_filename + "...")
    track.download(download_path)
    if convert_to_mp3:
        convert_mp4_to_mp3(download_path)
    print('file saved to {}'.format(download_path))


if __name__ == "__main__":
    download_destination = r'c:/tmp/the beatles (remastered)י'
    html_path = 'https://www.youtube.com/playlist?list=OLAK5uy_njHTOnoK_aQOAa3XvnvmzZ76n8cBIJquI'
    if str(html_path).find('playlist') != -1:
        download_youtube_playlist_to_mp3(html_path, download_destination)
    else:
        download_youtube_link_to_mp3(html_path, download_destination)
