from mss import mss

with mss() as sct:
    snapshot = sct.shot()
