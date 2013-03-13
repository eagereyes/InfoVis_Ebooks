#!/usr/bin/python
# coding=utf-8

# TODO:
# * remove references in square brackets
# * tweeting

# DB Schema:
# CREATE TABLE sources (id STRING PRIMARY KEY, venue STRING, year INTEGER, text BLOB);
# CREATE INDEX venue on sources (venue);
# CREATE INDEX year on sources (year);

from PyPDF2 import PdfFileReader
from zlib import compress, decompress
import sqlite3
import hashlib
import random
import sys

def ingestFile(venue, year, fileName, dbConn):
	pdf = PdfFileReader(open(fileName, 'rb'))
	# print len(pdf.pages)

	text = ''
	numPages = 0
	for page in pdf.pages:
		numPages += 1
		text += ' '+page.extractText()

	numChars = len(text)

	text = text.replace(u'Ô', '\'')
	text = text.replace(u'Õ', '\'')
	text = text.replace(u'Ó', '\'')
	text = text.replace(u'Ò', '\'')

#	text = compress(text.encode('ascii', 'xmlcharrefreplace'))

	md5 = hashlib.md5()
	md5.update(text.encode('ascii', 'ignore'))
	md5 = md5.hexdigest()

	dbConn.execute('INSERT INTO sources VALUES (?, ?, ?, ?)', (md5, venue, year, text))
	dbConn.commit()

	print 'Stored %s: %d pages, %d characters' % (fileName, numPages, numChars)


def sample(dbConn):
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

		sample = sample.strip()

		print sample


random.seed()

dbConn = sqlite3.connect('ebooks.sqlite')

if sys.argv[1] == 'ingest' and len(sys.argv) == 5:
	ingestFile(sys.argv[2], sys.argv[3], sys.argv[4], dbConn)
elif sys.argv[1] == 'sample':
	sample()
else:
	print 'Unknown operation'


