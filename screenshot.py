import numpy as np
from PIL import Image
import pytesseract
import mss
import time
import re

# The dimensions of the QWOP screen
QWOP_WIDTH = 640
QWOP_HEIGHT = 400

# Boolean controlling whether to repeatedly take screenshots (while runner is still alive)
is_alive = True

# Regex pattern to find the runner's distance
# FIXME: should the regex below not be: "\d+.*\d* metres"? since it could be a integer number of meters.
dist_pattern = re.compile("\-*\d+(\.\d+)? metres")
restart_pattern = re.compile("press")

# Sleep to allow user the time to navigate to the QWOP game
time.sleep(2)

""" Screen shot explanation: 

    =================================
    l###############################l
    l###############################l
    l########       o       ########l
    l########      /|\_     ########l
    l########      `/\      ########l
    l########      /  \     ########l
    l###############################l
    l###############################l
    =================================
                   | |
                   | |
                =========   
    
    # => cropped pixels
                  
    So the screenshot attempts to crop the surrounding sides of the screen off,
    leaving behind a QWOP_WIDTH x QWOP_HEIGHT size screenshot, hopefully 
    containing the QWOP man himself.
    
    Y tho?...
    
    This means less stuff to read through for the OCR, and thus faster
    screenshots!
    
    K.
"""


def calculate_cropped_box(sct):
    """ Calculate the dimensions of the cropped screenshot

    argument:
    sct -- an instance of mss.mss()
    """

    # Get the screen's details
    # returns {width, height, top, left} dictionary
    monitor = sct.monitors[1]
    # It looks like QWOP's screen is always centered
    # 'left' and 'top' calculates the left x-value and the top y-value of the required text in the game screen
    left = int((monitor["width"] - QWOP_WIDTH) / 2)
    top = int((monitor["height"] - QWOP_HEIGHT) / 2)
    # create a new bbox description that embodies the dimensions of the screenshot
    bbox = {"left": left, "top": top, "width": QWOP_WIDTH, "height": QWOP_HEIGHT}
    return bbox


with mss.mss() as sct:

    cropped_bbox = calculate_cropped_box(sct)

    while is_alive:
        # I had to do some elaborate screenshot conversions to get
        # 'mss' working with 'tesseract' OCR.

        grab = sct.grab(cropped_bbox)
        # Convert 'SnapShot' object to numpy array
        screen_array = np.array(grab)
        # Make a pillow image from the numpy array
        sct_img = Image.fromarray(screen_array)

        print("Performing OCR on the image...",)
        start_time = time.time()
        text = pytesseract.image_to_string(sct_img)
        end_time = time.time()
        print("Done\nOCR took {:.2f} seconds.\n".format(end_time - start_time))

        # Scan the screenshot to find how far the runner has come
        dist_match = dist_pattern.search(text)
        if dist_match:
            print(dist_match.group())
        else:
            print("Couldn't read the distance from the screenshot")

        # Scan the screenshot to find out if the runner has fallen
        is_alive = not restart_pattern.search(text)
        if ~is_alive:
            print("Runner has fallen")
