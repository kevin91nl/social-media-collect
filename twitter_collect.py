import logging
import os
import time
import tweepy
import json
import MySQLdb
import configparser
import argparse


class SQLListener(tweepy.StreamListener):
    def __init__(self, connection, time_limit=-1):
        self.start_time = time.time()
        self.connection = connection
        self.time_limit = time_limit
        self.cursor = self.connection.cursor()

    def on_exception(self, exception):
        logging.error(exception)

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            if '://' not in tweet['text']:
                print(tweet['text'])
                if self.time_limit != -1 and (time.time() - self.start_time) > self.time_limit:
                    return False

                if tweet['lang'] == 'en':
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S',
                                              time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
                    self.cursor.execute(
                        """INSERT INTO tweets(id, search, username, text, created_at) VALUES (%s, %s, %s, %s, %s)""",
                        (tweet['id'], 'bitcoin', tweet['user']['screen_name'], tweet['text'], timestamp))
                    self.connection.commit()
        except:
            pass
        return True

    def on_error(self, status):
        raise Exception('Got Twitter error! Error code: %s' % status)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Fetch message from Twitter and store them into a MySQL database.')
    parser.add_argument('ini', help='path to ini file')
    parser.add_argument('--timeout', help='number of second after which the script will stop', default=60, type=int)
    args = parser.parse_args()
    if not os.path.exists(args.ini):
        raise Exception('INI file %s does not exist' % args.ini)

    parser = configparser.ConfigParser()
    parser.read(args.ini)

    logging.basicConfig(filename=parser.get('logging', 'path'), level=logging.ERROR, format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    host = parser.get('database', 'host')
    user = parser.get('database', 'user')
    password = parser.get('database', 'password')
    database = parser.get('database', 'database')

    connection = MySQLdb.connect(host=host,
                                 user=user,
                                 passwd=password,
                                 db=database)
    connection.set_character_set('utf8')

    consumer_key = parser.get('twitter', 'consumer_key')
    consumer_secret = parser.get('twitter', 'consumer_secret')
    access_token = parser.get('twitter', 'access_token')
    access_token_secret = parser.get('twitter', 'access_token_secret')

    listener = SQLListener(connection, time_limit=args.timeout)

    # Authenticate
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Connect the stream to our listener
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=['bitcoin', 'blockchain', '-filter:retweets'])

    connection.close()
