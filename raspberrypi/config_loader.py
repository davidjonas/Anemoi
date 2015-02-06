import json

class ConfigLoader:
    def __init__(self, filename):
        f = open(filename, "r")
        jsonConfig = json.loads(f.read())
        self.websocket_port = jsonConfig['wbsocket_port']
        self.OSC_port = jsonConfig['OSC_port']
        self.AP_mode = jsonConfig['AP_mode']
        self.webserver = jsonConfig['webserver']
        self.sensor_name = jsonConfig['sensor_name']
        self.UDP_port = jsonConfig['UDP_port']
