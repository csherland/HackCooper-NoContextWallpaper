#!/usr/bin/python

from config import GMAIL, PW
import gspread.gspread as gspread
import json

SHEET_KEY = '0ApILAjelslrAdF9Wb0tqa3RWUHNYQWhFMm5UcG9UY0E'
QUOTE_FILE = 'static/quotes.json'

gc = gspread.login(GMAIL,PW)
sht1 = gc.open_by_key(SHEET_KEY)

worksheet = sht1.get_worksheet(0)

authors = worksheet.col_values(1)
quotes = worksheet.col_values(2)

authors = authors[1:]
quotes = quotes[1:]

x = list()
for i in range(len(authors)):
    x.append({'author':authors[i],'quote':quotes[i]})

f = open(QUOTE_FILE,'w')
f.write(json.dumps(x))

