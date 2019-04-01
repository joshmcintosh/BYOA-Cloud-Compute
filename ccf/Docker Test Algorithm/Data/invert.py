from PIL import Image
import PIL.ImageOps
import sys


def process(name):
    print(name)
    image = Image.open(str(name[0]))
    out = PIL.ImageOps.invert(image)
    out.save('fixed.jpeg')

def main():
    name = sys.argv[1:]
    process(name)

if __name__ == '__main__':
    main()