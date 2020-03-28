#!/usr/bin/env python3
import io
from sys import argv
from PIL import Image
from urllib import request


def color_27(image):
    w, h = image.size
    pix = image.load()
    for x in range(w):
        for y in range(h):
            pix[x, y] = tuple([0 if val < 85 else 255 if val > 170 else 127 for val in pix[x, y]])
    return image


def color_8(image):
    w, h = image.size
    pix = image.load()
    for x in range(w):
        for y in range(h):
            pix[x, y] = tuple([255 if val >= 128 else 0 for val in pix[x, y]])
    return image


def main():
    img = argv[1]
    img = Image.open(io.BytesIO(request.urlopen(img).read())) if "http" in img else Image.open(open(img, 'rb'))
    color_27(img).show()
    color_8(img).show()


if __name__ == "__main__":
    main()
