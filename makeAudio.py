"""
./makeAudio <post.json> <outFileName>

Outputs:
    - outFileName.mp3
"""
import ezcmdtools
from ezcmdtools import argument_types
import pyttsx3
import pathlib
import json

def validatePost(path: pathlib.Path):
    if not path.exists():
        return False
    try:
        post = json.loads(path.read_text())
        
        if type(post.get("text")) != str:
            return False
        return True
    except:
        return False

def main():
    rate = ezcmdtools.KeyedValue(argument_types.Integer, ("rate", "r"), 125)
    volume = ezcmdtools.KeyedValue(argument_types.Float, ("volume", "vol", "v" ), 1.0)
    voiceType = ezcmdtools.KeyedValue(argument_types.Enum("0", "1"), ("type", "t"), "0")
    postPath = ezcmdtools.Value(argument_types.ExistingFilePath)
    outFileName = ezcmdtools.Value(argument_types.Path, required=False, default=pathlib.Path(__file__).parent.joinpath("out.mp3"))
    

    helper_used, parsing_successful, reason = ezcmdtools.Parser().expect(
        postPath, outFileName,
        rate, volume, voiceType
    ).invalidate(
        ezcmdtools.Condition(lambda p:not validatePost(postPath.values[0])),
        f"Given json file is invalid!"
    ).invalidate(
        ezcmdtools.Condition(lambda p:rate.value <= 0), "Rate must be positive!"
    ).invalidate(
        ezcmdtools.Condition(lambda p: not (1 >= volume.value >= 0)), "Volume must be between 0 and 1!"
    ).parse()

    if helper_used:
        return

    if not parsing_successful:
        print("ERROR!", *reason.args)
        return


    post = json.loads(postPath.values[0].read_text())

    engine = pyttsx3.init() # object creation
    engine.setProperty('rate', rate.value)
    engine.setProperty('volume',volume.value)
    engine.setProperty('voice', engine.getProperty('voices')[int(voiceType.value)].id)

    engine.save_to_file(post["text"], outFileName.values[0].as_posix())
    engine.runAndWait()


if __name__ == '__main__':
    main()
