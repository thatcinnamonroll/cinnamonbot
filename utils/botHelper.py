import os

def ensureCacheDir():
    if not os.path.exists(".cache"):
        os.makedirs(".cache")
    if not os.path.exists(".cache/music"):
        os.makedirs(".cache/music")

def ensureDataDir():
    if not os.path.exists(".data"):
        os.makedirs(".data")
    dataJsons = {".data/settings.json":"utils/defSettings.json",".data/dictionary.json":"utils/dict.json"}
    for jsonToCheck in dataJsons:
        if not os.path.isfile(jsonToCheck):
            with open(dataJsons[jsonToCheck],"r") as defaultDataFile:
                with open(jsonToCheck,"w") as dataFile:
                    dataFile.write(defaultDataFile.read())
