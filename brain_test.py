"""
Some stuff for testing brain.py

This is some hacky crap. Redo later.
"""

import json
import serial
import time


def recordData(serialport="/dev/tty.usbserial-A7005EJD", serialspeed=9600
               count=100):
    """ Record data dumped by the NeuroSky headset into a set of nested lists.
        A delay more than 100ms between bytes (presumably, the time between 
        packets) starts the next list.
    """
    data = [[]]
    s = serial.Serial(port=serialport, baudrate=serialspeed)

    while len(data) < count:
        t0 = time.time()
        b = ord(s.read())
        t1 = time.time()
        if t1 - t0 > .1:
            data.append([])
        data[-1].append(b)
    
    return data


def dumpData(data, filename="data-dump.json"):
    """ 
    """
    with open(filename,'w') as f:
        json.dump(f, data)


class FakeSerial(object):
    """ A dummy serial connection that will stream data read from a file, one
        byte at a time. Built-in delays try to simulate communicating with
        the NeuroSky headset.
    """
    def __init__(self, filename="data-100.json"):
        with open(filename, 'r') as f:
            self.data = json.load(f)
        self.outerIter = iter(self.data)
        self.innerIter = iter(self.outerIter.next())
        self.closed = False

    def read(self):
        v = self.nextByte()
        return chr(v)

    def nextByte(self):
        try:
            time.sleep(0.0008)
            return self.innerIter.next()
        except StopIteration:
            try:
                self.innerIter = iter(self.outerIter.next())
                return self.innerIter.next()
            except StopIteration:
                time.sleep(1)
                self.outerIter = iter(self.data)
                self.innerIter = iter(self.outerIter.next())
                return self.innerIter.next()
            
