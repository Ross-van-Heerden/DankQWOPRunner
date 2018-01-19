import numpy as np
from PIL import Image
import pytesseract
from mss import mss
import time

# I think the QWOP screen is always this width
QWOP_WIDTH = 640

# sleep to allow user the time to navigate to the QWOP page
time.sleep(2)

with mss() as sct:
    # Get the screen's details
    monitor = sct.monitors[1] # returns {width, height, top, left} dictionary
    # It looks like QWOP's screen is always centered
    # 'left' calculates the left x-value of the game screen
    left = int((monitor["width"] - QWOP_WIDTH)/2)
    # create a new bbox description that embodies the dimensions of the screenshot
    cropped_bbox = {"left": left, "top": 0, "width": QWOP_WIDTH, "height": monitor["height"]}

    # Convert 'SnapShot' object to numpy array
    screen_array = np.array(sct.grab(cropped_bbox))

    frame = Image.fromarray(screen_array)
    
    print("Performing OCR on the image...",)
    start_time = time.time()
    text = pytesseract.image_to_string(frame)
    end_time = time.time()
    print("Done\nOCR took {:.2f} seconds.\n".format(end_time - start_time))

    print("Output:\n", text)

