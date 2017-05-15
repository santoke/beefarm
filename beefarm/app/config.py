import json

class Config:
    d = None

    def __init__(self):
        f = open('config/config.json')
        js = json.loads(f.read())
        f.close()
        Config.d = js