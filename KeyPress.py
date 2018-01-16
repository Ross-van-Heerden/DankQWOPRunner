from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

time.sleep(5)

# Press and release space
# keyboard.press(Key.space)
# keyboard.release(Key.space)

# Type w and o at the same time for 2 seconds
keyboard.press('w')
keyboard.press('o')

time.sleep(2)

keyboard.release('w')
keyboard.release('o')
