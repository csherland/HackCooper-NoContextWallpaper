# HackCooper - NoContext
# 2-8-14
# Add specified text to random image with random font

import urllib
import cStringIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

def addText(text):
    # Get an image
    imgFile = cStringIO.StringIO(urllib.urlopen('http://i.imgur.com/EpuhHJa.png').read())

    img = Image.open(imgFile)
    
    # Draw image and add the text 
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("sans-serif.ttf", 16)
    draw.text((0, 0), text, (255,255,255), font=font)
    img.save('static/img/sample-out.png')
