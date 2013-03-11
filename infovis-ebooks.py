#!/usr/bin/python

import pyPdf
import random
import sys

random.seed()
pdf = pyPdf.PdfFileReader(open(sys.argv[1], 'rb'))
# print len(pdf.pages)

text = ''
for page in pdf.pages:
	text += page.extractText()

pos = random.randrange(len(text))
sample = text[pos:pos+100]
sample = sample[sample.index(' ')+1:]
if sample.find('.') > 0:
	sample = sample[:sample.index('.')]
else:
	sample = sample[:sample.rindex(' ')]

print sample