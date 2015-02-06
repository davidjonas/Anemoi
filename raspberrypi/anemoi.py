from weather_station import WeatherStation
from broadcaster import Broadcaster
import time
import os
import sys
import logging
from config_loader import ConfigLoader
logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) == 2:
    conf = ConfigLoader(sys.argv[1])
else:
    conf = ConfigLoader("config.json")

if (conf.AP_mode):
    com = Broadcaster(host="localhost", port=conf.websocket_port)
else:
    com = Broadcaster(host=conf.webserver, port=conf.websocket_port)


def speedUpdate(value):
    global sound
    #print "Wind speed: %s" % value
    com.emit("windSpeedUpdate", {'value': value, 'id': id})

def directionUpdate(value):
    global sound
    #print "Wind direction: %s" % value
    com.emit("windDirectionUpdate", {'value': value, 'id': id})


ws = WeatherStation(windSpeedCallback=speedUpdate, windDirectionCallback=directionUpdate)
print "starting weather station thread."
ws.start()

com.wait_forever()

while True:
    try:
        time.sleep(25)
    except KeyboardInterrupt:
        break


print "Done, killing threads"
ws.kill()
