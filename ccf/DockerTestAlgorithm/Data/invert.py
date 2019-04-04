import sys

import PIL.ImageOps
from PIL import Image


def process(name):
    image = Image.open(str(name[0]))
    out = PIL.ImageOps.invert(image)
    out.save("ccf/Docker Test Algorithm/Data/fixed.jpeg")


def main():
    name = sys.argv[1:]
    process(name)


if __name__ == "__main__":
    main()
