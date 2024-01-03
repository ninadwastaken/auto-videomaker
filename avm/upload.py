from instagrapi import Client
import os

def upload(type, *args):
    if type == "instagram":
        instagram_upload(*args)
    elif type == "youtube":
        youtube_upload(*args)



def instagram_upload(path:str, caption:str):
    # path needs to be absolute path for some reason

    # env vars
    username = os.environ["INSTAGRAM_USERNAME"]
    password = os.environ["INSTAGRAM_PASSWORD"]

    cl = Client()
    cl.login(username, password)
    cl.clip_upload(path, caption)

    # delete thumbnail
    os.remove(f"{path}.jpg")

def youtube_upload():
    # TODO! write upload for yt channel
    pass


if __name__ == '__main__':
    instagram_upload(r"C:\Users\ninad\PycharmProjects\auto-video-maker\avm\media\1.mp4", "test2")
