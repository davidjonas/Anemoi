__author__ = 'David Jonas'

import sys
import time
from broadcaster import Broadcaster
import OSC
import time, random

port = 8080
host = "localhost"
last_dir = "N"


# tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
send_address = '127.0.0.1', 9000

# OSC basic client
c = OSC.OSCClient()
c.connect( send_address ) # set the address for all following messages


def sendWindSpeed(value):
    # single message
    msg = OSC.OSCMessage()
    msg.setAddress("/windSpeed") # set OSC address
    msg.append(value) # int
    c.send(msg)

def sendWindDirection(value):
    # single message
    msg = OSC.OSCMessage()
    msg.setAddress("/windDirection") # set OSC address
    msg.append(value) # string
    c.send(msg)


def updateSpeed(data):
    val = data["value"]
    sendWindSpeed(val)

def updateDirection(data):
    global last_dir
    global ac
    val = data["value"]
    #print "windDirection: %s" % val
    if val != last_dir:
        sendWindDirection(val)
    last_dir = val


print "Starting communications..."
com = Broadcaster(port=8080, host="192.168.42.1")
com.on("windSpeedUpdate", updateSpeed)
com.on("windDirectionUpdate", updateDirection)
print "communications established."
print "Enjoy..."

sendWindDirection("N")
sendWindSpeed(200)

com.wait_forever()

print "Finished"
