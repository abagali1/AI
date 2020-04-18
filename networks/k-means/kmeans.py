#!/usr/bin/env python3
import io
import random
from sys import argv
from PIL import Image
from time import time
from urllib import request


def dist(r, m):
    return (r[0] - m[0]) ** 2 + (r[1] - m[1]) ** 2 + (r[2] - m[2]) ** 2


def organize(previous_pixels, all_pixels):
    new_means, count = {}, 0
    for mean, pixs in previous_pixels.items():
        m = [0, 0, 0]
        for r, g, b, count in pixs[1]:
            m[0] += r * count
            m[1] += g * count
            m[2] += b * count
        m = (m[0] / pixs[0], m[1] / pixs[0], m[2] / pixs[0])

        new_means[m] = previous_pixels[mean]

    for pixel in all_pixels:
        new_mean, tmp = min(new_means.keys(), key=lambda m: dist(pixel, m)), (*pixel, all_pixels[pixel])
        current_mean = [x for x in new_means if tmp in new_means[x][1]][0]
        if new_mean != current_mean:
            new_means[current_mean][1].remove(tmp)
            new_means[new_mean][1].add(tmp)
            count += 1
    print("Moved: {}".format(count))
    return count == 0, new_means


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
    gen = 0
    while True:
        print("Gen: {}".format(gen))
        o = organize(kpixels, all_pixels)
        if o[0]:
            return kpixels
        else:
            kpixels = o[1]
        gen += 1

# def reconstruct(image, means):
#     w, h = image.size()
#     pix = image.load()
#     for x in range(w):
#         for y in range(h):
#             new_val = [x ]


def main():
    start = time()
    k, img = int(argv[1]), argv[2]
    img = Image.open(io.BytesIO(request.urlopen(img).read())) if "http" in img else Image.open(open(img, 'rb'))
    kmeanified = kmeans(k, img)
    print(time()-start)
    # reconstruct(img, kmeanified)


if __name__ == "__main__":
    main()
