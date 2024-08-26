import tomllib
from Utils import DotDict

def loadToml(configPath:str) -> DotDict:
    '''Load Toml data from file'''
    with open(configPath, 'rb') as file:
        data = DotDict(tomllib.load(file))
        print(f"Loaded Config File {configPath}")
        return data

def saveToml(configPath:str, data:DotDict):
    '''Save DotDict to Toml file'''
    with open(configPath, 'w') as file:
        tomllib.dump(data, file)

