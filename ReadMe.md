# InfoVis Ebooks
This script implements a simple Twitter bot that tweets random snippets from a database of text files.

To run, you will need to create a SQLite database using the following schema:

    CREATE TABLE sources (id STRING PRIMARY KEY, venue STRING, year INTEGER, origin STRING, fileName STRING);
    CREATE INDEX venue on sources (venue);
    CREATE INDEX year on sources (year);

# Commands
The script accepts a few simple commands:

* `ingest <Venue> <Year> <Origin> <File Name>` copies the content of the file into a compressed file in the sources directory and adds a new entry to the database. `Venue` and `year` are simple strings, and are currently unused. The idea is to later restrict tweeting to particular year ranges or venues. `Origin` is the place to link to when tweeting. This is currently a DOI in my use, but could be any URL.
* `sample` grabs a random snippet from the database and prints it.
* `tweet` tweets a random snippet. See below for Twitter settings.
* `tweet-maybe <probability>` tweets with a probability of 1-in-probability (so higher probability number actually means lower probability of tweet). The idea is to run the script on a regular basis from cron, but use the maybe function to make the tweets less regular.

# Twitter Settings

The script uses [Twython](https://github.com/ryanmcgrath/twython) for tweeting. For this to work, there needs to be a file `twitter.json` that contains a valid app key/secret pair, as well as an Oauth token/secret pair (see the file `twitter-sample.json`).

An application can be created on [Twitter's Developer site](https://dev.twitter.com), and for single-account use it's easy to create the tokens there as well (just make sure the app has write access so it can tweet!).