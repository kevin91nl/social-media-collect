import argparse
import configparser
import csv
import tweepy

TWEETS_PER_REQUEST = 100


class OutputWriter:
    fields = ['user', 'contributors', 'coordinates', 'created_at', 'favorite_count', 'favorited', 'geo', 'id', 'id_str',
              'in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id',
              'in_reply_to_user_id_str', 'is_quote_status', 'lang', 'retweet_count', 'retweeted', 'source',
              'source_url', 'text', 'truncated']

    def __init__(self, output_path, delimiter='\t'):
        output_file = open(output_path, 'w')
        self.writer = csv.DictWriter(output_file, fieldnames=self.fields, delimiter=delimiter)
        self.writer.writeheader()

    def write(self, tweet):
        values = {field: getattr(tweet, field) if hasattr(tweet, field) else None for field in self.fields}
        values['user'] = tweet.user.screen_name
        self.writer.writerow(values)


def fetch_by_ids(writer, input_path):
    print('Collecting Tweets using tweet identifiers from %s...' % input_path)
    tweet_ids = read_tweet_ids(input_path)
    print('%d tweet identifiers found...' % len(tweet_ids))
    tweet_chunks = list(chunks(tweet_ids, TWEETS_PER_REQUEST))
    for step, tweet_chunk in enumerate(tweet_chunks):
        print('Collecting bulk of %d Tweets (bulk %d out of %d)...' % (
            TWEETS_PER_REQUEST, step + 1, len(tweet_chunks)))
        tweets = api.statuses_lookup(tweet_chunk)
        for tweet in tweets:
            writer.write(tweet)


def fetch_by_users(writer, input_path):
    print('Collecting Tweets using Twitter users found in %s...' % input_path)
    users = read_twitter_users(input_path)
    print('%d users found...' % len(users))
    all_tweets = []
    for user in users:
        new_tweets = api.user_timeline(screen_name=user, count=200)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
        while len(new_tweets) > 0:
            new_tweets = api.user_timeline(screen_name=user, count=200, max_id=oldest)
            all_tweets.extend(new_tweets)
            oldest = all_tweets[-1].id - 1
            print("%s tweets downloaded so far %s..." % (len(all_tweets), user))
    for tweet in all_tweets:
        writer.write(tweet)


def read_tweet_ids(path):
    """
    Read all tweet ids contained in a file.

    :param path: The path to the file containing tweet ids
    :return: A list of found tweet identifiers
    """
    tweet_ids = []
    with open(path, 'rb') as input_file:
        input_data = input_file.read().decode('utf8')
        for line in input_data.split("\r\n")[1:]:
            parts = line.split("\t")
            if len(parts) == 3 and len(parts[1]) >= 18 and parts[1].isdigit():
                tweet_ids.append(parts[1])
    return tweet_ids


def read_twitter_users(path):
    """
    Read all Twitter users specified per line in a text file.

    :param path: A path to the file
    :return: List of the found Twitter users
    """

    users = []
    with open(args.users, 'r') as input_file:
        input_data = input_file.readlines()
        for line in input_data:
            line = line.strip()
            if len(line) > 0:
                users.append(line)

    return users


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect Tweets.')
    parser.add_argument('ini', help='File to the INI file containing the Twitter configuration.')
    parser.add_argument('output', help='The path to the CSV file in which the Tweets will be stored.')
    parser.add_argument('--delimiter', help='Delimiter used in the output CSV.', default='\t')

    subparsers = parser.add_subparsers()

    parser_tweet_ids = subparsers.add_parser('fetch_by_ids', description='Fetch Tweets by a file containing tweet identifiers.')
    parser_tweet_ids.add_argument('input', help='The path to the input file containing Tweet identifiers.')
    parser_tweet_ids.set_defaults(action='fetch_by_ids')

    parser_users = subparsers.add_parser('fetch_by_users', description='Fetch Tweets by a file containing Twitter usernames.')
    parser_users.add_argument('users', help='The path to the input file containing Twitter usernames per line.')
    parser_users.set_defaults(action='fetch_by_users')

    args = parser.parse_args()
    writer = OutputWriter(args.output, args.delimiter)

    parser = configparser.ConfigParser()
    parser.read(args.ini)
    consumer_key = parser.get('twitter', 'consumer_key')
    consumer_secret = parser.get('twitter', 'consumer_secret')
    access_token = parser.get('twitter', 'access_token')
    access_token_secret = parser.get('twitter', 'access_token_secret')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    if args.action == 'fetch_by_ids':
        fetch_by_ids(writer, args.input)

    elif args.action == 'fetch_by_users':
        fetch_by_users(writer, args.users)

    print('Done! Results collected in %s' % args.output)