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

	# Get fonts and pick a random one
	ttffiles = [ f for f in listdir('static/fonts') if isfile(join('static/fonts',f)) ]    
	randfile = randint(0,len(ttffiles))

	# Get an image
	imgFile = cStringIO.StringIO(urllib.urlopen('http://i.imgur.com/vzD8A.jpg').read())

	img = Image.open(imgFile)
	# Draw image and add the text 
	draw = ImageDraw.Draw(img)
	fonturlf='static/fonts/' + ttffiles[randfile]
	font = ImageFont.truetype(fonturlf, 72)

	y_text = 0
	for line in lines:
		[width, height] = font.getsize(line)
		draw.text((0, y_text), line, (255,255,255), font=font)
		y_text += height

	
	img.save('static/img/sample-out.png')
