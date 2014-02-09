#!/usr/bin/python
import praw

porn = ['earthporn','waterporn','skyporn','spaceporn','fireporn','destructionporn','geologyporn','cityporn','villageporn','abandonedporn','infrastructureporn','machineporn','militaryporn','cemeteryporn','architectureporn','animalporn','botanicalporn','humanporn','adrenalineporn','climbingporn','culinaryporn','designporn','albumartporn','metalporn','geekporn','roomporn','instrumentporn','macroporn','microporn','artporn','fractalporn','exposureporn','streetartporn','historyporn','mapporn','newsporn','futureporn','fossilporn']

r = praw.Reddit('hackcooper')
f = open('static/js/photolinks.txt', 'a+')
for sub in porn:
	submissions = r.search('[800x600]', subreddit=sub, sort='top', syntax=None, period='all', limit=10)
	for x in submissions:
		exten = str(x.url)
		exten = exten.lower()
		if exten.find('.png') > -1 or exten.find('.jpg') > -1:
			f.write(x.url)
			f.write('\n')
f.close()