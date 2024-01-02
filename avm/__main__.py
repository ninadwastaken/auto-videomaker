import ezcmdtools
from ezcmdtools import argument_types, gate_sizes
from .extra import YoutubeLink, PositiveInteger, Fraction
from sys import stderr

mode = ezcmdtools.Value(
    argument_types.Enum("create", "download", "upload", "config", "clear")
)
background_video_download_link = ezcmdtools.Value(
    YoutubeLink,
    required=False
)
clear_command_target = ezcmdtools.Value(
    argument_types.Enum("media", "output"),
    required=False
)



background_download_resolution = ezcmdtools.KeyedValue(
    argument_types.Enum("4320p", "2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "any"),
    names=("resolution", "res"),
    default="any"
)

subreddit = ezcmdtools.KeyedValue(
    argument_types.String,
    names=("subreddit", "sr"),
    default="stories"
)
word_count_range = ezcmdtools.Gate(
    PositiveInteger,
    gate_sizes.Atmost(2),
    names=("length", "len", "l")
)

voice_rate = ezcmdtools.KeyedValue(
    PositiveInteger,
    names=("rate", "r"),
    default=125
)
voice_volume = ezcmdtools.KeyedValue(
    Fraction,
    names=("volume", "vol", "v" ),
    default=1.0
)
voice_type = ezcmdtools.KeyedValue(
    argument_types.Enum("0", "1"),
    names=("type", "t"),
    default="0"
)

max_count = ezcmdtools.KeyedValue(
    PositiveInteger,
    names=("count", "c"),
    default=float("inf")
)


suppress_warning = ezcmdtools.Flag(("quiet", "q"))


# region preparser
_, _, _ = (
    ezcmdtools.Parser()
    .set_flavour()
    .set_rules(suppress_warnings=True)
    .expect(suppress_warning)
    .parse()
)
# endregion

# region parser
helper_used, parsing_successful, reason = (
    ezcmdtools.Parser()
    .set_flavour()
    .set_policies()
    .set_rules(
        suppress_warnings=suppress_warning.is_set
    )
    # .set_helper(None)
    
    .expect(
        mode, background_video_download_link, clear_command_target, max_count,
        background_download_resolution,
        subreddit, voice_rate, voice_volume, voice_type,
        word_count_range,
        suppress_warning
    )
    
    .invalidate(
        ezcmdtools.Condition(lambda p: mode.values[0] == "download" and not background_video_download_link.is_set), "Valid youtube video link was not provided to download"
    )
    .invalidate(
        ezcmdtools.Condition(lambda p: mode.values[0] == "clear" and not clear_command_target.is_set), "Valid target was not provided to clear"
    )

    # .inform(
    #     None, None
    # )

    .parse()
)
# endregion

if helper_used:
    raise NotImplementedError("Helpers not implemented vro")

if not parsing_successful:
    print("ERROR!", *reason.args, file=stderr)
    exit(1)

if mode.values[0] == "create":
    from .create import create
    create(
        subreddit_name=subreddit.value,
        voice_rate=voice_rate.value, voice_type=int(voice_type.value), voice_volume=voice_volume.value,
        word_count_range=(0 if word_count_range.count < 1 else word_count_range.values[0], float("inf") if word_count_range.count < 2 else word_count_range.values[1]),
        max_count=max_count.value
    )

elif mode.values[0] == "download":
    from .download import download
    download(link=background_video_download_link.values[0], resolution=background_download_resolution.value)

elif mode.values[0] == "upload":
    pass

elif mode.values[0] == "config":
    pass

elif mode.values[0] == "clear":
    from .clear import clear
    clear(clear_command_target.values[0])

else:
    print(f"ERROR! Unexpected value for mode `{mode.values[0]}`!", file=stderr)
    exit(1)

