#!/usr/bin/env python3

import sys
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from unicornhatmini import UnicornHATMini

unicornhatmini = UnicornHATMini()
display_width, display_height = unicornhatmini.get_shape()
print("{}x{}".format(display_width, display_height))

font = ImageFont.truetype("5x7.ttf", 8)

text = datetime.now().strftime("%I:%M")

text_width, text_height = font.getsize(text)
print(f"text width: {text_width}")

image = Image.new('P', (text_width, display_height), 0)
draw = ImageDraw.Draw(image)
draw.text((0, -1), text, font=font, fill=255)
for y in range(display_height):
    for x in range(display_width):
         if image.getpixel((x, y)) == 255:
             unicornhatmini.set_pixel(x, y, 0, 128, 0)
         else:
             unicornhatmini.set_pixel(x, y, 0, 0, 0)
unicornhatmini.show()
time.sleep(10)
