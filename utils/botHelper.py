import os

def ensureCacheDir():
    if not os.path.exists(".cache"):
        os.makedirs(".cache")
    if not os.path.exists(".cache/music"):
        os.makedirs(".cache/music")

def ensureDataDir():
    if not os.path.exists(".data"):
        os.makedirs(".data")
    if not os.path.isfile(".data/settings.json"):
        with open("utils/defSettings.json","r") as defaultSettingsFile:
            with open(".data/settings.json","w") as settingsFile:
                settingsFile.write(defaultSettingsFile.read())
