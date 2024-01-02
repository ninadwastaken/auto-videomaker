import requests
from pathlib import Path
import pyttsx3
from sys import stderr
from moviepy.editor import AudioFileClip, VideoFileClip
from sortedcontainers import SortedKeyList
from random import randrange, seed

def get_posts(subreddit_name):
    try:
        auth = requests.auth.HTTPBasicAuth("igvNsz7UvomjacrasRXFPA","HK9ivn3H_GodvOq79g4qhii8VvUA1A")
        headers = {"User-Agent":"MyAPI/0.0.1"}
        tok = requests.post(
            'https://www.reddit.com/api/v1/access_token', 
            auth=auth, data={"grant_type":"password", "username":"Denviser", "password":"hello1234"}, 
            headers=headers
        ).json()['access_token']
        headers.update({'Authorization':f'bearer {tok}'})
        res = requests.get(f'https://oauth.reddit.com/r/{subreddit_name}/hot', headers=headers).json()

        return [
            {
                "subreddit": post['data']['subreddit'],
                "title": post['data']['title'],
                "text": post['data']['selftext']
            } for post in res['data']['children']
        ]
    
    except Exception as e:
        print(f"ERROR! Could not get posts from {subreddit_name}", file=stderr)
        print(e, file=stderr)
        exit(1)

def is_valid(post: dict, word_count_range: tuple[int, int]):
    # TODO! Check whether the post has already been used or if word count is invalid
    # Consider just using the title of the post
    return True

def create(
        subreddit_name: str,
        voice_rate: int, voice_type: int, voice_volume: float,
        word_count_range: tuple[int, int],
        max_count: int
):
    seed(None)

    # TODO: Consider making the shit below more readable plz ;-;

    outdir = Path(__file__).parent.joinpath("output")
    file_start_index_no = len(list(outdir.glob('*')))
    completed_videos = 0

    try:
        bg_videos: list[VideoFileClip] = SortedKeyList(
            (VideoFileClip(path.as_posix()).without_audio()
            for path in Path(__file__).parent.joinpath("media").glob("*")),
            key=lambda item: item.duration
        )
    except Exception as e:
        print("ERROR! Could not load downloaded background videos", file=stderr)
        print(e)
        exit(1)

    if not bg_videos:
        print("ERROR! No downloaded background videos found", file=stderr)
        exit(1)    

    bg_video_count = len(bg_videos)

    audio_engine = pyttsx3.init()
    audio_engine.setProperty('rate', voice_rate)
    audio_engine.setProperty('volume', voice_volume)
    audio_engine.setProperty('voice', audio_engine.getProperty('voices')[voice_type].id)

    tmp_file = Path(__file__).parent.joinpath("tmp", "test.mp3")

    for post in get_posts(subreddit_name):
        if not is_valid(post, word_count_range):
            continue

        if completed_videos >= max_count:
            break

        print(f"Trying to create video for post titled `{post['title']}`")

        output_name = f"{completed_videos + file_start_index_no}.mp4"

        audio_engine.save_to_file(f'{post["title"]} ... {post["text"]} .....', tmp_file.as_posix())
        audio_engine.runAndWait()

        audio_clip = AudioFileClip(tmp_file.as_posix())
        vid_length = audio_clip.duration
        
        left = bg_videos.bisect_key_left(vid_length)
        if left == bg_video_count:
            audio_clip.close()
            print(f"WARNING: Could not find background clip to fit length `{vid_length}`")
            continue
        
        bg_clip: VideoFileClip = bg_videos[randrange(left, bg_video_count)]
        clip_start_timestamp = randrange(0, int(bg_clip.duration - vid_length) + 1)
        bg_clip = bg_clip.subclip(clip_start_timestamp, clip_start_timestamp + vid_length)

        # TODO! Add text to bg clip

        bg_clip.set_audio(audio_clip).write_videofile(outdir.joinpath(output_name).as_posix(), logger=None)
        print(f"Created video `{output_name}`")

        audio_clip.close()
        completed_videos += 1
    
    print(f"Successfully created {completed_videos} videos")
    tmp_file.unlink()
        
        