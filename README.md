PyBrain
=======

A simple library for reading data from a NeuroSky-based EEG headset.

Specifically, this was designed for reading data from toys using the low-end
version of the NeuroSky chipset. While it generates data in the same packet
format, the low-end chipset appears to only support a subset of the content
generated by the full version.

The library does not itself specifically require a serial library (e.g. 
PySerial). The serial connection object is passed to the `Brain` constructor,
and it is up to the user of the library to actually create it. The standard
NeuroSky chipset, at least in the first generation of toy headsets,
communicates at 9600 baud, no parity, 8 bits, 1 stop bit.

Requires Python 2.6 to 2.7.

brain.py
--------

`brain.py` implements the `Brain` class, a subclass of `Thread`. A `Brain` 
object, running as a thread, reads bytes from the serial port as they arrive. 
Full packets' checksums are verified, and valid packets are sent to the Brain's
`packetHandler()` method. The raw contents of checksum-failing packets are
sent to its `checksumFailHandler()`. These can be overridden in a
`Brain` subclass, or `Brain` can be instantiated as-is, with alternate
handler functions supplied as arguments.

brain_test.py
-------------

This is not (currently) a real unit test; it is just a couple of small
functions that can be used for testing things that use `Brain`. Of most
interest is the `FakeSerial` object: a serial port simulator that feeds canned 
data read from a file (`data-100.json` by default, also in the repo). This
will let you work on stuff without having to wear the headset the whole time.

