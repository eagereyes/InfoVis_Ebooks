#!/usr/bin/python

# TODO:
# * check out argparse: http://docs.python.org/2.7/library/argparse.html
# * remove references in square brackets
# * fix apostrophes and quotation marks
# * SQLite database
# * tweeting

from PyPDF2 import PdfFileReader
import random
import sys

random.seed()

pdf = PdfFileReader(open(sys.argv[1], 'rb'))
# print len(pdf.pages)

text = ''
for page in pdf.pages:
	text += page.extractText()

for i in range(10):
	pos = random.randrange(len(text))
	length = random.randrange(50, 100)
	sample = text[pos:pos+length]
	sample = sample[sample.index(' ')+1:]
	if sample.find('.') > 0:
		sample = sample[:sample.index('.')]
	else:
		sample = sample[:sample.rindex(' ')]

	# Quality criteria? Try again if sample is shorter than five characters, etc.

	print sample
