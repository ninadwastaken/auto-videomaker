from pytube import YouTube
from pathlib import Path
from sys import stderr

def download(link: str, resolution: str):
    yt = YouTube(link)
    outdir = Path(__file__).parent.parent.joinpath("media")
    name = f"{len(list(outdir.glob('*')))}.mp4"
    try:
        yt.streams.filter(file_extension='mp4', res=resolution if resolution != "any" else None)[0].download(filename=outdir.joinpath(name).as_posix())
    except Exception as e:
        print(f"ERROR! Could not download youtube video (`{link}`)", file=stderr)
        print(e, file=stderr)
        exit(1)
    
    print(f"Successfully downloaded video (`{link}`) as `{name}`")