#!/usr/bin/python
# coding=utf-8

# TODO:
# * remove references in square brackets
# * tweeting

# DB Schema:
# CREATE TABLE sources (id STRING PRIMARY KEY, venue STRING, year INTEGER, origin STRING, fileName STRING);
# CREATE INDEX venue on sources (venue);
# CREATE INDEX year on sources (year);

import sqlite3
import hashlib
import gzip
from random import seed, randrange
from twython import Twython
import json

import sys

PATH = 'sources/'

def ingestFile(venue, year, origin, fileName, dbConn):

	with open(fileName) as inFile:
		text = ''
		numLines = 0
		for line in inFile:
			numLines += 1
			text += ' '+line

		numChars = len(text)

		md5 = hashlib.md5()
		utext = text.decode('utf-8')
		md5.update(utext.encode('ascii', 'ignore'))
		md5 = md5.hexdigest()

		outFileName = '%s-%s-%s.txt.gz' % (venue, year, md5)
		outFile = gzip.open(PATH + outFileName, 'wb')
		outFile.write(utext.encode('utf-8', 'ignore'))
		outFile.close()

		dbConn.execute('INSERT OR REPLACE INTO sources VALUES (?, ?, ?, ?, ?)', (md5, venue, year, origin, outFileName))
		dbConn.commit()

		print 'Stored %s: %d lines, %d characters' % (fileName, numLines, numChars)


def sample(dbConn):
	sources = []
	for row in dbConn.execute('select id, fileName, origin from sources'):
		sources.append({'id': row[0], 'fileName': row[1], 'origin': row[2]})

	source = sources[randrange(len(sources))]

	txtFile = gzip.open(PATH + source['fileName'])
	text = txtFile.read()
	txtFile.close()

#	print text

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

	return '%s - %s' % (sample, source['origin'])

def tweet(dbConn):
	text = sample(dbConn)

	twitterAppData = json.load(open('twitter.json'))
	twitter = Twython(app_key = twitterAppData['app_key'],
            app_secret = twitterAppData['app_secret'],
            oauth_token = twitterAppData['oauth_token'],
            oauth_token_secret = twitterAppData['oauth_token_secret'])

	twitter.updateStatus(status=text)


#
# Main
#

seed()

dbConn = sqlite3.connect('ebooks.sqlite')

if sys.argv[1] == 'ingest' and len(sys.argv) == 6:
	# venue, year, origin, fileName
	ingestFile(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], dbConn)
elif sys.argv[1] == 'sample':
	print sample(dbConn)
elif sys.argv[1] == 'tweet':
	tweet(dbConn)
else:
	print 'Unknown operation'


