import argparse
from PIL import Image
import numpy as np

## Program Flow ##
# Read args
# Load image
# Build colour map
# Create BW image
# Place full-brightness coloured dot in centre of map grid
##################

## TODO: Uncompress script

def avgPX(*args ):
    output = [0, 0, 0]

    # Add 
    for arg in args[0]:
        output[0] += arg[0]
        output[1] += arg[1]
        output[2] += arg[2]
    
    # Average
    output[0] = round(output[0] / len(args[0]))
    output[1] = round(output[1] / len(args[0]))
    output[2] = round(output[2] / len(args[0]))

    return output
    # return (0,0,0)

## Create an args parser ##
parser = argparse.ArgumentParser()
parser.add_argument("img", help="Path to desired image")
parser.add_argument("msize", help="Size of colour map (NxN px squares)")
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

# pixel_map = []
args.msize = int(args.msize)
print(args.msize)

out = []

q_lock = False

for i, row in enumerate(raw_im):

    cl = []
    for j, col in enumerate(row):
        
        if (i % args.msize) + (j % args.msize) == (args.msize * 2) - 2:
            # Append avg
            prev_px = []

            for k in range(args.msize):
                prev_px.append(raw_im[i][j - k])
            
            # print(avgPX(prev_px))
            if not q_lock:
                cl.append((0, 0, 255))
                q_lock = True
            else:
                cl.append(avgPX(prev_px))
        else:
            # Append the L value

            R = col[0]
            G = col[1]
            B = col[2]
            
            # Calc L
            L = round(R * 299 / 1000 + G * 587 / 1000 + B * 114 / 1000)
            
            cl.append((L, L, L))

    out.append(cl)

## Output image ##
arr = np.array(out, dtype=np.uint8)
im2 = Image.fromarray(arr)

imname = args.img.split(".")
im2.save( imname[0] + ".bw." + imname[len(imname) - 1])