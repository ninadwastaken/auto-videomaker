from ezcmdtools.argument_types import Type

@Type
def YoutubeLink(arg: str):
    from re import search
    # https://stackoverflow.com/a/67255602
    pattern = "^(?:https?:)?(?:\/\/)?(?:youtu\.be\/|(?:www\.|m\.)?youtube\.com\/(?:watch|v|embed)(?:\.php)?(?:\?.*v=|\/))([a-zA-Z0-9\_-]{7,15})(?:[\?&][a-zA-Z0-9\_-]+=[a-zA-Z0-9\_-]+)*(?:[&\/\#].*)?$"
    
    if search(pattern, arg) is not None:
        return arg
    return None

@Type
def PositiveInteger(arg: str):
    if arg.lower() == "inf":
        return float("inf")
    return int(arg) if int(arg) > 0 else None

@Type
def Fraction(arg: str):
    return float(arg) if 0 <= float(arg) <= 1 else None
