import argparse
import configparser

import re
import tweepy

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect Tweets by a file containing Tweet identifier.')
    parser.add_argument('ini', help='File to the INI file containing the Twitter configuration.')
    parser.add_argument('input', help='The path to the input file containing Tweet identifiers.')
    parser.add_argument('output', help='The path to the CSV file in which the Tweets will be stored.')
    args = parser.parse_args()

    parser = configparser.ConfigParser()
    parser.read(args.ini)
    consumer_key = parser.get('twitter', 'consumer_key')
    consumer_secret = parser.get('twitter', 'consumer_secret')
    access_token = parser.get('twitter', 'access_token')
    access_token_secret = parser.get('twitter', 'access_token_secret')

    with open(args.input, 'rb') as input_file:
        input_data = input_file.read().decode('utf8')
        tweet_ids = list(set(re.findall(r"\d{18,}", input_data)))

    consumer_key = parser.get('twitter', 'consumer_key')
    consumer_secret = parser.get('twitter', 'consumer_secret')
    access_token = parser.get('twitter', 'access_token')
    access_token_secret = parser.get('twitter', 'access_token_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweet = api.get_status(tweet_ids[-1])
    print(tweet.json)