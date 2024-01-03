from instagrapi import Client
import os

def upload():
    username = ""
    password = ""
    cl = Client()
    cl.login(username, password)


def instagram_upload(path:str, caption:str):
    # path needs to be absolute path for some reason
    username = os.environ["INSTAGRAM_USERNAME"]
    password = os.environ["INSTAGRAM_PASSWORD"]
    cl = Client()
    cl.login(username, password)
    cl.clip_upload(path, caption)

def youtube_upload():
    # TODO! write upload for yt channel
    pass


if __name__ == '__main__':
    instagram_upload(r"C:\Users\ninad\PycharmProjects\auto-video-maker\avm\media\1.mp4", "test1")
