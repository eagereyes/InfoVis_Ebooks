#!/usr/bin/python
# coding=utf-8

# TODO:
# * remove references in square brackets
# * tweeting

# DB Schema:
# CREATE TABLE sources (id STRING PRIMARY KEY, venue STRING, year INTEGER, fileName STRING);
# CREATE INDEX venue on sources (venue);
# CREATE INDEX year on sources (year);

from PyPDF2 import PdfFileReader
import sqlite3
import hashlib
import gzip
from random import seed, randrange
import sys

PATH = 'sources/'

def ingestFile(venue, year, fileNames, dbConn):
	for fileName in fileNames:

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

		md5 = hashlib.md5()
		md5.update(text.encode('ascii', 'ignore'))
		md5 = md5.hexdigest()

		outFileName = '%s-%s-%s.txt.gz' % (venue, year, md5)
		txtFile = gzip.open(PATH + outFileName, 'wb')
		txtFile.write(text.encode('utf-8', 'ignore'))
		txtFile.close()

		dbConn.execute('INSERT OR REPLACE INTO sources VALUES (?, ?, ?, ?)', (md5, venue, year, outFileName))
		dbConn.commit()

		print 'Stored %s: %d pages, %d characters' % (fileName, numPages, numChars)


def sample(dbConn):
	sources = []
	for row in dbConn.execute('select id, fileName from sources'):
		sources.append({'id': row[0], 'fileName': row[1]})

	source = sources[randrange(len(sources))]

	txtFile = gzip.open(PATH + source['fileName'])
	text = txtFile.read()
	txtFile.close()

	print text

	for i in range(10):
		pos = randrange(len(text))
		length = randrange(50, 100)
		sample = text[pos:pos+length]
		sample = sample[sample.index(' ')+1:]
		if sample.find('.') > 0:
			sample = sample[:sample.index('.')]
		else:
			sample = sample[:sample.rindex(' ')]

		sample = sample.strip()

		# Quality criteria? Try again if sample is shorter than five characters, etc.

		print sample


seed()

dbConn = sqlite3.connect('ebooks.sqlite')

if sys.argv[1] == 'ingest' and len(sys.argv) >= 5:
	ingestFile(sys.argv[2], sys.argv[3], sys.argv[4:], dbConn)
elif sys.argv[1] == 'sample':
	sample(dbConn)
elif sys.argv[1] == 'rescan':
	# rescan files and populate DB
	pass
else:
	print 'Unknown operation'


