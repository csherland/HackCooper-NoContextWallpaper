# HackCooper - NoContext
# 2-8-14
# Add specified text to random image with random font

import urllib
import cStringIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

def addText(text, imgurl, fonturl):
    # Get an image
    imgFile = cStringIO.StringIO(urllib.urlopen('http://i.imgur.com/vzD8A.jpg').read())

    img = Image.open(imgFile)
    
    # Draw image and add the text 
    draw = ImageDraw.Draw(img)
    fonturlf='static/fonts/AUGUSTUS.TTF'
    font = ImageFont.truetype(fonturlf, 42)
    draw.text((0, 0), text, (255,255,255), font=font)
    img.save('static/img/sample-out.png')
