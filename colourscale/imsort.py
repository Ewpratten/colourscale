import argparse
from PIL import Image
import numpy as np

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

def write(im, name, imname):
    arr = np.array(im, dtype=np.uint8)
    im2 = Image.fromarray(arr)

    im2.save(imname[0] + name + imname[len(imname) - 1])

def csort(inp):
    return sorted(inp, key=Keys.lum)

def clsort(img):
    output = []
    # for row in img:
    return sorted(img, key=lambda x: (avg(x)))

# def 




## Create an args parser ##
parser = argparse.ArgumentParser()
parser.add_argument("img", help="Path to desired image")
args = parser.parse_args()

## Load the image ##
try:
    im = Image.open(args.img)
except FileNotFoundError:
    print("Invalid file")
    exit(1)
print(f"Loaded {args.img}")

## Build colour map ##
raw_im = np.asarray(im)

## Detect spacing ##
# spac = 0
# while True:
#     if raw_im[spac][spac][2] == 255:
#         break
#     else:
#         spac += 1
# spac += 1

# print(spac)

## Build squash_im ##
sr_im = []

for i, row in enumerate(raw_im):
    # sr_cl = []

    sr_im.append(csort(row))

    # for j, col in enumerate(row):

    #     # Build squash
    #     if (i % spac) + (j % spac) == (spac * 2) - 2:

    #         # Check bounds
    #         if j <= spac:
    #             sr_cl.append((col[0], col[1], col[2]))
    #         else:
    #             # Expand
    #             prev = row[j - spac]
    #             curr = col

    #             for k in range(spac):
    #                 val = [0, 0, 0]
    #                 val[0] = scl(prev[0], curr[0], spac, k)
    #                 val[1] = scl(prev[1], curr[1], spac, k)
    #                 val[2] = scl(prev[2], curr[2], spac, k)

    #                 itp = (val[0], val[1], val[2])
    #                 lv = clrz(row[j-k][0])
    #                 # itp = (0,0,0)
    #                 sr_cl.append(cbn(itp, lv))

    #             # sr_cl.append(clrz(curr[0]))

    # if sr_cl != []:
    #     sr_im.append(sr_cl)

sr_im = clsort(sr_im)

## Output image ##
imname = args.img.split(".")

write(sr_im, ".sr.", imname)
