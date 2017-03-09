import argparse
import configparser
import csv
import tweepy

TWEETS_PER_REQUEST = 100


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


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

    tweet_ids = []
    with open(args.input, 'rb') as input_file:
        input_data = input_file.read().decode('utf8')
        for line in input_data.split("\r\n")[1:]:
            parts = line.split("\t")
            if len(parts) == 3 and len(parts[1]) >= 18 and parts[1].isdigit():
                tweet_ids.append(parts[1])
    tweet_chunks = list(chunks(tweet_ids, TWEETS_PER_REQUEST))

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    fields = ['user', 'contributors', 'coordinates', 'created_at', 'favorite_count', 'favorited', 'geo', 'id', 'id_str',
              'in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id',
              'in_reply_to_user_id_str', 'is_quote_status', 'lang', 'retweet_count', 'retweeted', 'source',
              'source_url', 'text', 'truncated']
    print('Collecting Tweets using data from %s (and configuration from %s)...' % (args.input, args.ini))
    with open(args.output, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fields)
        writer.writeheader()
        for step, tweet_chunk in enumerate(tweet_chunks):
            print('Collecting bulk of %d Tweets (bulk %d out of %d)...' % (TWEETS_PER_REQUEST, step + 1, len(tweet_chunks)))
            tweets = api.statuses_lookup(tweet_chunk)
            for tweet in tweets:
                values = {field: getattr(tweet, field) if hasattr(tweet, field) else None for field in fields}
                values['user'] = tweet.user.screen_name
                writer.writerow(values)
    print('Done! Results collected in %s' % args.output)
