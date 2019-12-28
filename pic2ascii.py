from __future__ import print_function
from PIL import Image, ImageEnhance
import sys

# This line contains all of the values associated with grayscale tones in an array indexed at 0 (so 0 is |=a, 1 is |=b, etc)
bwvals = ["|=a","|=b","|=c","|=d","|=e","|=f","|=g","|=h","|=i","|=j","|=k","|=l","|=m","|=n","|=o","|=p","|=q","|=r","|=s","|=t","|=u","|=v","|=w","|=x","|=y","|=z","|=z"]
charwidth = 46

# This function opens the file resizes it according to a hard-coded value (currently 50) for width, and returns it as an array of arrays
def getPixels(filename):
    img = Image.open(filename, 'r')
    benhancer = ImageEnhance.Brightness(img)
    brighter = benhancer.enhance(1.5)
    w, h = img.size
    scaling = charwidth/float(w)
    resized = brighter.resize((charwidth,int(round(scaling*h*6/11))),Image.NEAREST)
    w, h = resized.size
    pix = list(resized.getdata())
    return [pix[n:n+w] for n in range(0, w*h, w)]

# This function gets called every time to convert from 0-255 values to 0-5 values
def musifyrgb(raw):
    return round(raw/51)

# This function only gets called if musifyrgb returns 000,111,222,333,444, or 555
def musifybw(raw):
    bwval = int(round((raw+1)/30))
    return bwvals[bwval]

# This function checks musifyrgb and calls musifybw if necessary, returning either the grayscale code or the heximal rgb code
# Returns something in format |=i or |345
def calculateMuseCode(r, g, b):
    (mr, mg, mb) = (musifyrgb(r), musifyrgb(g), musifyrgb(b))
    if mr == mg and mr == mb:
        totalrgb = r + g + b
        musecode = musifybw(totalrgb)
    else:
        musecode = "|%d%d%d" % (mr, mg, mb)
    return musecode


# This returns an array with width elements
def processRow(row):
    prevcode = ""
    output = []
    for (r, g, b) in row:
        currcode = calculateMuseCode(r, g, b)
        if currcode == prevcode and currcode != "|=a":
            output.append("")
        else:
            output.append(currcode)
            prevcode = currcode
    return output

# The result of this is an array with height elements, each element is an array with width elements
def processImage(rows):
    return [processRow(row) for row in rows]

# This function makes it go
if __name__ == "__main__":
    filename = sys.argv[1]
    rows = processImage(getPixels(filename))
    for row in rows:
        for pixel in row:
            if pixel == "|=a":
                print("|_", end='')
            else:
                print("%s@" % pixel, end='')
        print("|/", end='')

# =a 00 = 0 (aka 0)              5f (aka 1) = 95
# =b 08 = 8                     87 (aka 2) = 135
# =c 12 = 18                    af (aka 3) = 175
# =d 1C = 28                    d7 (aka 4) = 215
# =e 26 = 38
# =f 30 = 48
# =g 3A = 58
# =h 44 = 68
# =i 4E = 78
# =j 58 = 88
# =k 62 = 98
# =l 6C = 108
# =m 76 = 118
# =n 80 = 128
# =o 8A = 138
# =p 94 = 148
# =q 9E = 158
# =r A8 = 168
# =s B2 = 178
# =t BC = 188
# =u C6 = 198
# =v D0 = 208
# =w DA = 218
# =x E4 = 228
# =y EE = 238
# =z FF = 255 (aka 5)
