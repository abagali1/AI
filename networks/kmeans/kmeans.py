#!/usr/bin/env python3
import io
from sys import argv
from PIL import Image
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

    random_means = [x[0] for x in sorted([*pixel_count.items()], key=lambda x: x[1])[-k:]]
    organized = {}
    for pixel in all_pixels:
        key = min(random_means, key=lambda x: dist(pixel, x))
        if key in organized:
            if pixel not in organized[key][1]:
                organized[key][0] += pixel_count[pixel]
                organized[key][1].add(pixel)
        else:
            organized[key] = [pixel_count[pixel], {pixel}]

    while True:
        o = reorganize(organized, pixel_count)
        if o[0]:
            return organized, pixel_count
        else:
            organized = o[1]


def reconstruct(image, means):
    w, h = image.size
    pix = image.load()
    for x in range(w):
        for y in range(h):
            pix[x, y] = tuple(map(round, [m for m in means if pix[x, y] in means[m][1]][0]))
    return image


def bfs(pic, start, w, h):
    queue, visited = [start], {start}
    color = pic[start]

    for x, y in queue:
        for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1),
                         (x - 1, y - 1)]:
            if 0 <= neighbor[0] < w and 0 <= neighbor[1] < h and pic[neighbor] == color and neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
    return visited


def connected_components(image):
    visited, components = set(), {}
    w, h = image.size
    pix = image.load()
    for x in range(w):
        for y in range(h):
            if (x, y) in visited:
                continue
            tmp = bfs(pix, (x, y), w, h)
            visited |= tmp
            if pix[x, y] in components:
                components[pix[x, y]] += 1
            else:
                components[pix[x, y]] = 1
    return components


def main():
    k, img = int(argv[1]), argv[2]
    img = Image.open(io.BytesIO(request.urlopen(img).read())) if "http" in img else Image.open(open(img, 'rb'))
    kmeanified, pixel_count = kmeans(k, img)
    new_image = reconstruct(img, kmeanified)
    new_image.save("kmeans/2021abagali.png", "PNG")

    most_common_pixel = max(pixel_count, key=pixel_count.get)
    size = img.size
    print("Size: {} x {}".format(*size))
    print("Pixels: {}".format(size[0] * size[1]))
    print("Distinct Pixel Count: {}".format(len(pixel_count)))
    print("Most common pixel: {} => {}".format(most_common_pixel, pixel_count[most_common_pixel]))
    print("Final means: ")
    for count, kmean in enumerate(kmeanified):
        print("{}: {} => {}".format(count + 1, kmean, sum(pixel_count[x] for x in kmeanified[kmean][1])))
    print("Region counts: {}".format(', '.join([str(x) for x in connected_components(new_image).values()])))


if __name__ == "__main__":
    main()
