#!/usr/bin/env python3
import io
import random
from sys import argv
from PIL import Image
from urllib import request

def dist(r, m):
    return (r[0]-m[0])**2 + (r[1]-m[1])**2 + (r[2]-m[2])**2


def kmeans(k, image):
    w, h = image.size
    pix = image.getdata()
    means = {random.choice(pix): [] for _ in range(k)}
    for pixel in pix:
        means[min(means, key=lambda x: dist(pixel, x))].append(pixel)
    new_means = {}
    for mean, vals in means.items():
        key = (sum(x[0] for x in vals), sum(x[1] for x in vals), sum(x[2] for x in vals))





def main():
    k, img = argv[1], argv[2]
    img = Image.open(io.BytesIO(request.urlopen(img).read())) if "http" in img else Image.open(open(img, 'rb'))
    kmeans(k, img)


if __name__ == "__main__":
    main()
