import cv2
from PIL import Image
import numpy as np

cam = cv2.VideoCapture(0)



## Keys ##
class Keys(object):
    overall = lambda x: (int(x[0]) + int(x[1]) + int(x[2]))
    red = lambda x: (int(x[0]))
    green = lambda x: (int(x[1]))
    blue = lambda x: (int(x[2]))
    avg = lambda x: (int(x[0]) + int(x[1]) + int(x[2])) / 3
    lum = lambda x: round(int(x[0]) * 299 / 1000 + int(x[1]) * 587 / 1000 + int(x[2]) * 114 / 1000)


def avg(li):
    output = 0
    for i in li:
        x = i
        output += round(int(x[0]) * 299 / 1000 + int(x[1]) * 587 / 1000 + int(x[2]) * 114 / 1000)
    return output / len(li)

def csort(inp):
    return sorted(inp, key=Keys.lum)

def clsort(img):
    output = []
    # for row in img:
    return sorted(img, key=lambda x: (avg(x)))

## Load the image ##
while True:
    ret_val, im = cam.read()

    ## Build colour map ##
    raw_im = np.asarray(im)

    sr_im = []

    for i, row in enumerate(raw_im):

        sr_im.append(sorted(row, key=Keys.lum))

    # sr_im.append((0,0,0))
    sr_im = clsort(sr_im)

    out_im = np.array(sr_im)

    cv2.imshow("out", out_im)

    if cv2.waitKey(1) == 27: 
            break  # esc to quit
cv2.destroyAllWindows()