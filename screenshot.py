import numpy as np
from PIL import Image
import pytesseract
import mss
import time
import re

# I think the QWOP screen is always this width
QWOP_WIDTH = 640

# Boolean controlling whether to repeatedly take screenshots
continuous = True

# Regex pattern to find the runner's distance
# FIXME: should the regex below not be: "\d+.*\d* metres"? since it could be a integer number of meters.
dist_pattern = re.compile("\-*\d+(\.\d+)? metres")

# Sleep to allow user the time to navigate to the QWOP game
time.sleep(2)

""" Screen shot explanation: 

    =================================
    l########               ########l
    l########               ########l
    l########       o       ########l
    l########      /|\_     ########l
    l########      `/\      ########l
    l########      /  \     ########l
    l########               ########l
    l########               ########l
    =================================
                   | |
                   | |
                =========   
    
    # => cropped pixels
                  
    So the screenshot attempts to crop the 
    left and right sides of the screen off,
    leaving behind a QWOP_WIDTH wide column down the middle, hopefully 
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
    # 'left' calculates the left x-value of the game screen
    left = int((monitor["width"] - QWOP_WIDTH)/2)
    # create a new bbox description that embodies the dimensions of the screenshot
    bbox = {"left": left, "top": 0, "width": QWOP_WIDTH, "height": monitor["height"]}
    return bbox

with mss.mss() as sct:

    cropped_bbox = calculate_cropped_box(sct)

    while continuous:
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
