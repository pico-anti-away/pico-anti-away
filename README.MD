## What is this?

The finished device keeps computer sessions active.

Mounts to the computer as an HID keyboard and sends a non used international keystroke to the computer 1-5 times, with a .1-.5 second delay, every 10-30 seconds.  One LED lights up when it's turned on, the other flashes when a keystroke is sent.

![Finished example](example.jpg)

#### --Note that once code is loaded onto Pico, it will stop mounting as a storage device, so code cannot be modified unless a hard reset (found in troubleshooting) is performed.--
#### To disable this behavior, comment out lines in boot.py

#### Parts needed
- Pi Pico
- 2 standard LEDs
- 1 Mechanical Keyboard Switch
- 2 resistors (I used 250 ohm)
- Some wire
- 3d Printer

#### Printing the case:
Remixed from https://www.thingiverse.com/thing:5233768 by EG3Dprinting
1. Load pico_case_bottom and pico_case_top in your slicer
2. Generate the gcode, no supports needed
3. Print it

#### Soldering config:

1.  Solder resistors of choice to positive legs of LEDs
2.  Solder key blink LED positive leg to GP2 and negative leg to GND
3.  Solder status LED positive leg to GP16 and negative leg to GND
4.  Pull keyboard button wires through top of case, then solder to ground and GP22

#### Pi Pico config:

1. Hold down button on Pi Pico, plug in while continuing to hold
2. While continuing to hold, wait for Pi to appear as a drive on computer
3. Move .uf2 in root of this repo to root of Pi Pico
4. Wait for device to reboot
5. Place all files found in Pico Files on root of Pi Pico

#### Troubleshooting:

Debug messages can be viewed by opening a serial monitor on the COM port the device connects itself as.

A hard reset can be performed by connecting to the Pico on the COM port the device connects itself as, with speed 115200.  If using PUTTY, set Serial Line to COM#, Speed 115200, Connection Type: Serial, then run these commands:

    >>> import storage
    >>> storage.erase_filesystem()

If the keystroke causes issues, another key can be substituted.  keyboard_keys_hid.py has all variable to key mappings.

If you'd rather download your own libraries instead of using the ones included here, check README-other.md
