#!/usr/bin/env python3
import io
import random
from sys import argv
from PIL import Image
from urllib import request


def dist(r, m):
    return (r[0] - m[0]) ** 2 + (r[1] - m[1]) ** 2 + (r[2] - m[2]) ** 2


def organize(means, pixels):
    new_means = {}
    for mean, pixs in pixels.items():
        m = (sum(r[0] * r[3] for r in pixs[1]) / pixs[0], sum(g[1] * g[3] for g in pixs[1]) / pixs[0],
             sum(b[2] * b[3] for b in pixs[1]) / pixs[0])
        new_means[m] = pixels[mean]


def kmeans(k, image):
    data, all_pixels = [*image.getdata()], {}
    for x in data:
        if x in all_pixels:
            all_pixels[x] += 1
        else:
            all_pixels[x] = 1

    means, kpixels = [random.choice(data) for _ in range(k)], {}
    for pixel in all_pixels:
        key = min(means, key=lambda m: dist(pixel, m))
        if key in kpixels:
            kpixels[key][0] += all_pixels[pixel]
            kpixels[key][1].add((*pixel, all_pixels[pixel]))
        else:
            kpixels[key] = [all_pixels[pixel], {(*pixel, all_pixels[pixel])}]
    print(kpixels)
    organize(means, kpixels)


def main():
    random.seed(1)
    k, img = int(argv[1]), argv[2]
    img = Image.open(io.BytesIO(request.urlopen(img).read())) if "http" in img else Image.open(open(img, 'rb'))
    kmeans(k, img)


if __name__ == "__main__":
    main()
