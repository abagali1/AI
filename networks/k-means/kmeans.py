#!/usr/bin/env python3
import io
from sys import argv
from PIL import Image
from urllib import request


def main():
    k, img = argv[1], argv[2]
    img = Image.open(io.BytesIO(request.url(image).read())) if "http" in image else Image.open(open(image, 'rb'))


if __name__ == "__main__":
    main()
