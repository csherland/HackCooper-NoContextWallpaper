# HackCooper - NoContext
# 2-8-14
# Add specified text to random image with random font

import urllib
import cStringIO
from PIL import Image, ImageFont, ImageDraw, ImageFilter 
from os import listdir
from os.path import isfile, join
from random import randint
import textwrap

def addText(text, author, imgurl):
	lines = textwrap.wrap(text, width = 40)

    # Get an image
	imgFile = cStringIO.StringIO(urllib.urlopen(imgurl).read())

	# Get fonts and pick a random one
	ttffiles = [f for f in listdir('fonts') if isfile(join('fonts',f))]
	randfile = randint(0,len(ttffiles)-1)

	# Get an image
	imgFile = cStringIO.StringIO(urllib.urlopen(imgurl).read())

	img = Image.open(imgFile)
	# Draw image and add the text 
	draw = ImageDraw.Draw(img)
	fonturlf='fonts/' + ttffiles[randfile]
	fontsize = 150
	font = ImageFont.truetype(fonturlf, fontsize)

	y_text = 0
	i=0
	x=0
	y=0
	width0=0
	author = '-' + author
	[widthauthor, height] = font.getsize(author)
	for line in lines:
		if i == 0:
			[width0,height0]=font.getsize(line)
			[imgwidth,imgheight] = img.size
			if (width0 > imgwidth) or (height0*len(lines)+1 > imgheight) or (widthauthor > imgwidth):
				while (width0 > imgwidth) or (height0*len(lines)+1 > imgheight) or (widthauthor > imgwidth):
					fontsize = fontsize - 1
					font = ImageFont.truetype(fonturlf, fontsize)
					[width0,height0]=font.getsize(line)
				x=0
				y=randint(0,imgheight-(height0*(len(lines)+1)))
			else:
				x=randint(0,imgwidth-width0)
				y=randint(0,imgheight-(height0*(len(lines)+1)))
		[width, height] = font.getsize(line)
		draw.text((x-2, y-2), line, (0,0,0), font=font)
		draw.text((x+2, y-2), line, (0,0,0), font=font)
		draw.text((x-2, y+2), line, (0,0,0), font=font)
		draw.text((x+2, y+2), line, (0,0,0), font=font)
		draw.text((x, y), line, (255,255,255), font=font)
		y += height
		i = i + 1
	x = x+width0-widthauthor
	draw.text((x-2, y-2), author, (0,0,0), font=font)
	draw.text((x+2, y-2), author, (0,0,0), font=font)
	draw.text((x-2, y+2), author, (0,0,0), font=font)
	draw.text((x+2, y+2), author, (0,0,0), font=font)
	draw.text((x,y), author, (255,255,255), font=font)
	
	output = cStringIO.StringIO()
	img.save(output, "JPEG", option='optimize')
	img = output.getvalue()
	output.close()

	return img
