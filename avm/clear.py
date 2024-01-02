from pathlib import Path

targetMap = {
    "media": Path(__file__).parent.joinpath("media"),
    "output": Path(__file__).parent.joinpath("output"),
}

def clear(target: str):
    targetPath = targetMap[target]

    for path in targetPath.glob("*"):
        if path.is_file():
            path.unlink()
    
    print(f"Successfully cleared {target}")
    