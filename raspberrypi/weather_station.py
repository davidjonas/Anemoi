# -*- coding: utf-8 -*-
__author__ = 'David Jonas'

import time
import RPi.GPIO as GPIO
import threading
import spidev


class WeatherStation(threading.Thread):

    timesToChange = 3
    currentDir = 0
    nextDir = 0
    counterTimesRep = 0
    NUMDIRS = 8
    #there was a problem with the wind direction function. The values were never arriving to 220.
    #multiplying the values to this factor solved the problem
    clippingFactor = 1.25
    #ADC readings:
    #These directions match 1-for-1 with the values in adc, but
    #will have to be adjusted as noted above. Modify 'dirOffset'
    #to which direction is 'away' (it's West here).
    #adc = [26, 45, 77, 118, 161, 196, 220, 256]
    #with this small adjustment we had better results detecting northwest
    adc = [26, 45, 77, 118, 161, 186, 220, 256]
    strVals = ["W","NW","N","SW","NE","S","SE","E"]
    dirOffset = 0
    STEP = 1000
    last_rev = 0
    revs = 0
    current = int(time.time()*1000)
    nextStep = current + STEP
    val = 1
    prevVal = 1
    speedPin = 27
    directionChannel = 0
    _windSpeedCallbacks = []
    _windDirectionCallbacks = []
    exitFlag = False
    spi = None

    def __init__(self, speedPin = 27, directionChannel = 0, windSpeedCallback = None, windDirectionCallback = None):
        threading.Thread.__init__(self)
        self.speedPin = speedPin
        self.directionChannel = directionChannel
        self.spi = spidev.SpiDev()

        if windSpeedCallback is not None:
            self._windSpeedCallbacks.append(windSpeedCallback)
        else:
            self._windSpeedCallbacks = []

        if windDirectionCallback is not None:
            self._windDirectionCallbacks.append(windDirectionCallback)
        else:
            self._windDirectionCallbacks = []

    def run(self):
        #Wind direction setup
        self.spi.open(0,0)
        GPIO.setmode(GPIO.BCM)

        #Wind speed reading
        GPIO.setup(self.speedPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        while True:
            if self.exitFlag:
                break
            self.current = int(time.time()*1000)
            self._speed_interrupt()
            if self.current > self.nextStep:
                self._on_wind_speed_update(self._calcSpeed())
                self._on_wind_direction_update(self._calcWindDir(0))
                self.nextStep = self.current + self.STEP
            time.sleep(0.1)

        GPIO.cleanup()

    def _read_channel(self, channel):
        adcLocal = self.spi.xfer2([1,(8+channel)<<4,0])
        data = ((adcLocal[1]&3) << 8) + adcLocal[2]
        return data

 
    def _calcWindDir(self, channel):
        val = self._read_channel(channel)

        #Shift to 255 range
        val >>= 2
        reading = float(val*self.clippingFactor)
        
        #Look the reading up in directions table. Find the first value
        #that's >= to what we got.
        for x in range(len(self.adc)):
            if self.adc[x] >= reading:
                break
        x = (x + self.dirOffset) % 8
        if x !=  self.currentDir:
            if x !=  self.nextDir:
                    self.nextDir = x
                    self.counterTimesRep = 1
            else:
                if self.counterTimesRep >= self.timesToChange:
                    self.counterTimesRep = 0
                    self.currentDir = self.nextDir
                    self.nextDir = -1
                else:
                    self.counterTimesRep=self.counterTimesRep+1                

        return self.strVals[x]
     
    def _speed_interrupt(self):
        self.val = GPIO.input(self.speedPin)
        if self.prevVal == 1 and self.val == 0:
            if self.last_rev == 0:
                self.last_rev = time.time()
                self.revs = 0
            else:
                currentTime = time.time()
                self.revs = 1.0 / (currentTime - self.last_rev)
                self.last_rev = time.time()

        self.prevVal = self.val

    def _calcSpeed(self):
        base = 24011.0
        speed = base * self.revs
        self.revs = 0
        return speed / 1000

    def add_wind_speed_callback(self, callback):
        self._windSpeedCallbacks.append(callback)

    def add_wind_direction_callback(self, callback):
        self._windDirectionCallbacks.append(callback)

    def _on_wind_speed_update(self, value):
        for cb in self._windSpeedCallbacks:
            cb(value)

    def _on_wind_direction_update(self, value):
        for cb in self._windDirectionCallbacks:
            cb(value)

    def kill(self):
        self.exitFlag = True