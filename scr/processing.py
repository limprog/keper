
from PIL import Image
import sys
import os
import random


def open_screen(filepath):
    try:
        tatras = Image.open(filepath)
    except IOError:
        print("Unable to load image")
        sys.exit(1)


def gray(image):
    process_image = image.convert('L')


def resize(image):
    width, height = image.size
    new_width = 100  # ширина
    new_height = int(new_width * height / width)
    process_image = image.resize((new_width, new_height), Image.ANTIALIAS)


def crop(image):
    process_image = image.crop((random.randint(0,1080), random.randint(0,1920), random.randint(0,1080), random.randint(0,1920)))


def rotate(image):
    process_image = image.rotate(random.randint(0,270))