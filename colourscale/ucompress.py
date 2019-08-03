import argparse
from PIL import Image
import numpy as np

def write(im, name, imname):
    arr = np.array(im, dtype=np.uint8)
    im2 = Image.fromarray(arr)

    im2.save(imname[0] + name + imname[len(imname) - 1])

def scl(s, e, r, ip):
    s = int(s)
    e = int(e)
    m = ((e - s) / (r - 0))
    return (m * ip)

def clrz(L):
    R = (.33 * L) / (299 / 1000)
    G = (.33 * L) / (587 / 1000)
    B = (.33 * L) / (114 / 1000)
    # R * 299 / 1000 + G * 587 / 1000 + B * 114 / 1000

    return (R, G, B)

def cbn(p1, p2):
    R = min((p1[0] + p2[0]), 255)
    G = min((p1[1] + p2[1]), 255)
    B = min((p1[2] + p2[2]), 255)

    return (R, G, B)

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
spac = 0
while True:
    if raw_im[spac][spac][2] == 255:
        break
    else:
        spac += 1
spac += 1

print(spac)

## Build squash_im ##
sq_im = []

for i, row in enumerate(raw_im):
    sq_cl = []
    for j, col in enumerate(row):

        # Build squash
        if (i % spac) + (j % spac) == (spac * 2) - 2:
            
            # Check bounds
            if j <= spac:
                sq_cl.append((col[0], col[1], col[2]))
            else:
                # Expand
                prev = row[j - spac]
                curr = col

                for k in range(spac):
                    val = [0, 0, 0]
                    val[0] = scl(prev[0], curr[0], spac, k)
                    val[1] = scl(prev[1], curr[1], spac, k)
                    val[2] = scl(prev[2], curr[2], spac, k)

                    itp = (val[0], val[1], val[2])
                    lv = clrz(row[j-k][0])
                    # itp = (0,0,0)
                    sq_cl.append(cbn(itp, lv))

                # sq_cl.append(clrz(curr[0]))
    

    if sq_cl != []:
        sq_im.append(sq_cl)
# print(sq_im)

## Output image ##
imname = args.img.split(".")

write(sq_im, ".sq.", imname)