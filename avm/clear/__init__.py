from pathlib import Path

targetMap = {
    "media": Path(__file__).parent.parent.joinpath("media"),
    "output": Path(__file__).parent.parent.joinpath("output"),
}

def clear(target: str):
    targetPath = targetMap[target]

    for path in targetPath.glob("*"):
        if path.is_file():
            path.unlink()
    
    print(f"Successfully cleared {target}")
    