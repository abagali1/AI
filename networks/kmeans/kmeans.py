#!/usr/bin/env python3
import io
import random
from sys import argv
from PIL import Image
from time import time
from urllib import request


def dist(r, m):
    return (r[0] - m[0]) ** 2 + (r[1] - m[1]) ** 2 + (r[2] - m[2]) ** 2


def reorganize(previous, pixel_count):
    new, moved = {}, 0
    for mean, pixels in previous.items():
        m = [0, 0, 0]
        for pixel in pixels[1]:
            occurrences = pixel_count[pixel]
            m[0] += pixel[0] * occurrences
            m[1] += pixel[1] * occurrences
            m[2] += pixel[2] * occurrences
        new[(m[0] / pixels[0], m[1] / pixels[0], m[2] / pixels[0])] = previous[mean]

    means = [*new.keys()]
    for pixel in pixel_count:
        new_mean = min(means, key=lambda x: dist(pixel, x))
        current_mean = [x for x in new if pixel in new[x][1]][0]
        if new_mean != current_mean:
            new[current_mean][0] -= pixel_count[pixel]
            new[current_mean][1].remove(pixel)
            new[new_mean][0] += pixel_count[pixel]
            new[new_mean][1].add(pixel)
            moved += 1
    return moved == 0, new


def kmeans(k, image):
    all_pixels, pixel_count = [*image.getdata()], {}
    for x in all_pixels:
        if x in pixel_count:
            pixel_count[x] += 1
        else:
            pixel_count[x] = 1

    random_means = random.choices(all_pixels, k=k)
    organized = {}
    for pixel in all_pixels:
        key = min(random_means, key=lambda x: dist(pixel, x))
        if key in organized:
            if pixel not in organized[key][1]:
                organized[key][0] += pixel_count[pixel]
                organized[key][1].add(pixel)
        else:
            organized[key] = [pixel_count[pixel], {pixel}]

    for m in organized:
        assert organized[m][0] == sum(pixel_count[x] for x in organized[m][1])

    gen = 0
    while True:
        o = reorganize(organized, pixel_count)
        if o[0]:
            return organized, pixel_count
        else:
            organized = o[1]
        gen += 1


def reconstruct(image, means):
    w, h = image.size
    pix = image.load()
    for x in range(w):
        for y in range(h):
            pix[x, y] = tuple(map(round, [m for m in means if pix[x, y] in means[m][1]][0]))
    return image


def main():
    start = time()
    random.seed(1738114)
    k, img = int(argv[1]), argv[2]
    img = Image.open(io.BytesIO(request.urlopen(img).read())) if "http" in img else Image.open(open(img, 'rb'))
    kmeanified, pixel_count = kmeans(k, img)
    reconstruct(img, kmeanified).save("kmeans/2021abagali.png", "PNG")

    most_common_pixel = max(pixel_count, key=pixel_count.get)
    print("Size: {} x {}".format(*img.size))
    print("Pixels: {}".format(len(img.getdata())))
    print("Distinct Pixel Count: {}".format(len(pixel_count)))
    print("Most common pixel: {} => {}".format(most_common_pixel, pixel_count[most_common_pixel]))
    print("Final means: ")
    for count, kmean in enumerate(kmeanified):
        print("{}: {} => {}".format(count+1, kmean, sum(pixel_count[x] for x in kmeanified[kmean][1])))


if __name__ == "__main__":
    main()
