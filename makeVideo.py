"""
./makeVideo <youtubelink> <timestamp> <audiofile_path> <outPutName>

Ouptuts:
funal video
"""
from moviepy.editor import *
from pytube import YouTube
import os


def downloadBgVid(link):
    
    yt = YouTube(link)
    
    try:
        yt.streams.filter(file_extension='mp4', res='720p')[0].download(filename='bg.mp4')
    except Exception as e:
        print('f scene')


def getBg(timestamp, audiofile_path):

    vid_length = AudioFileClip(audiofile_path).duration
    bg_clip = VideoFileClip("bg_vid.mp4").subclip(timestamp, vid_length).without_audio()
    
    return bg_clip


def makeVideo(link, timestamp, audiofile_path, outPutName):

    downloadBgVid(link)

    video_clip = getBg(timestamp, audiofile_path)
    
    #add text


    


    #adding audio
    audio_clip = AudioFileClip(audiofile_path)
    video_clip.audio = audio_clip

    video_clip.write_videofile(outPutName + ".mp4")