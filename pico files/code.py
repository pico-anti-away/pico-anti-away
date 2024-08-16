import random
import usb_hid
import digitalio
import time
import board
import asyncio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from keyboard_keys_hid import *

KEY_TO_PRESS = KEY_INT6  # gotten from keyboard_keys_hid

INIT = False 
STATUS = False  # Determines if the device is on or off at start

KEY_BLINK_LED = None
STATUS_LED = None
BUTTON = None
KBD = None

def init_board_components():
    global KEY_BLINK_LED, BUTTON, STATUS_LED, KBD

    while not INIT:
        try:
            KEY_BLINK_LED = digitalio.DigitalInOut(board.GP16)
            KEY_BLINK_LED.direction = digitalio.Direction.OUTPUT
            KEY_BLINK_LED.value = True

            STATUS_LED = digitalio.DigitalInOut(board.GP2)
            STATUS_LED.direction = digitalio.Direction.OUTPUT
            STATUS_LED.value = True

            BUTTON = digitalio.DigitalInOut(board.GP22)
            BUTTON.direction = digitalio.Direction.INPUT
            BUTTON.pull = digitalio.Pull.UP

            break

        except Exception as e:
            print("Error initializing components:", e)
            KEY_BLINK_LED = None
            STATUS_LED = None
            BUTTON = None
            print("Waiting 1s and attempting again")

def init_kbd():
    global KBD
    while True:
        try:
            KBD = Keyboard(usb_hid.devices) # init if status = true 
            break
        except:
            print("could not init kbd, waiting and retrying")
            time.sleep(1)


def main():
    global KBD

    time.sleep(3) # 3 second wait after power is received before registering as HID
    init_board_components()
    init_kbd()

    loop = asyncio.get_event_loop()
    loop.create_task(button_handler())
    loop.create_task(press_key())
    loop.run_forever()

async def key_led_blink():
    if KEY_BLINK_LED is None:
        return

    KEY_BLINK_LED.value = not KEY_BLINK_LED.value
    await asyncio.sleep(0.02)
    KEY_BLINK_LED.value = not KEY_BLINK_LED.value

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

            except:
                init_kbd()

        else:
            print("Button off")
            await asyncio.sleep(2)

async def button_handler():
    global STATUS
    global KBD
    
    last_button_state = True  # Assume the button is not pressed initially
    debounce_delay = 0.05     # 50 ms debounce time

    while True:
        if BUTTON is None:
            return

        current_button_state = BUTTON.value

        # Detect a button press (transition from high to low)
        if current_button_state == False and last_button_state == True:
            await asyncio.sleep(debounce_delay)  # Wait for debounce delay
            if BUTTON.value == False:  # Confirm the button is still pressed after the debounce delay
                
                STATUS = not STATUS
                print("Button pressed - value is ", BUTTON.value, " status is ", STATUS)

                STATUS_LED.value = not STATUS

        last_button_state = current_button_state

        await asyncio.sleep(0.1)  # Polling interval to check the button state

async def led_flash(interval):
    while True:
        if STATUS_LED is None or KEY_BLINK_LED is None:
            return

        KEY_BLINK_LED.value = not KEY_BLINK_LED.value
        await asyncio.sleep(interval)
        KEY_BLINK_LED.value = not KEY_BLINK_LED.value

main()
