
Pi Pico config (if not using libs included in this github for whatever reason)):

1. Hold down button on Pi Pico, plug in while continuing to hold
2. While continuing to hold, wait for Pi to appear as a drive on computer
3. Move .uf2 file of latest CircuitPython installation onto the root of the Pi Pico's drive
    Find download here: https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython
4. Download libs from https://circuitpython.org/libraries
5. Place the adafruit_hid library in the libs folder
6. Place adafruit_ticks.mpy in the libs folder
7. Download asyncio from https://pypi.org/project/adafruit-circuitpython-asyncio/#files
8. Place asyncio folder in the libs folder - i have no idea where this came from
9.  Place keyboard_keys_hid.py in the root of the Pi Pico's drive
10. Place code.py in the root of the Pi Pico's drive