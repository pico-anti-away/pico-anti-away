import random
import usb_hid
import digitalio
import board
import asyncio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from keyboard_keys_hid import *

KEY_TO_PRESS = KEY_INT6  # gotten from keyboard_keys_hid

# Initialize LEDs and button
try:
    KEY_BLINK_LED = digitalio.DigitalInOut(board.GP2)
    KEY_BLINK_LED.direction = digitalio.Direction.OUTPUT

    STATUS_LED = digitalio.DigitalInOut(board.GP16)
    STATUS_LED.direction = digitalio.Direction.OUTPUT

    BUTTON = digitalio.DigitalInOut(board.GP28)
    BUTTON.direction = digitalio.Direction.INPUT
    BUTTON.pull = digitalio.Pull.DOWN
    
except Exception as e:
    print("Error initializing components:", e)
    KEY_BLINK_LED = None
    STATUS_LED = None
    BUTTON = None

STATUS = True  # init to true

def main():
    global KBD 

    if KEY_BLINK_LED is None or STATUS_LED is None or BUTTON is None:
        return
    KBD = Keyboard(usb_hid.devices)
    print("init kbd", KBD)
    
    loop = asyncio.get_event_loop()
    loop.create_task(button_handler())
    loop.create_task(press_key())
    loop.run_forever()

async def key_led_blink():
    if KEY_BLINK_LED is None:
        return
    
    KEY_BLINK_LED.value = True
    await asyncio.sleep(0.05)
    KEY_BLINK_LED.value = False

async def press_key():
    while True:
        if STATUS:
            try:
                num_key_presses = random.randint(1, 5)
                print("kpress", num_key_presses)
                
                for _ in range(num_key_presses):
                    KBD.press(KEY_TO_PRESS)
                    KBD.release_all()
                    
                    key_delay = random.uniform(0.1, 0.5)
                    print("kdlay", key_delay)
                    await key_led_blink()
                    await asyncio.sleep(key_delay)

                key_interval = random.uniform(5, 25)
                print("kint", key_interval)
                await asyncio.sleep(key_interval)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print("Error:", e)
                await led_flash(1)
        else:
            print("button off")
            await asyncio.sleep(1)

async def button_handler():
    while True:
        if BUTTON is None:
            return
        
        if BUTTON.value:
            global STATUS
            STATUS = not STATUS
            print("BUTTON", STATUS)
            
            if STATUS:
                STATUS_LED.value = True
            else:
                STATUS_LED.value = False
        await asyncio.sleep(0.25)

async def led_flash(interval):
    while True:
        if STATUS_LED is None or KEY_BLINK_LED is None:
            return
        
        STATUS_LED.value = not STATUS_LED.value
        KEY_BLINK_LED.value = not KEY_BLINK_LED.value
        await asyncio.sleep(interval)

main()