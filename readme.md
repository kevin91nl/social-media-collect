# Social Media Collect
The goal of this collection of scripts is to simplify the collection of social media documents, such as Tweets and Facebook posts.

## Installation
Make sure to use Python 3. This can be done by either installing Python 3 or using a virtual environment. Then, install the requirements by using the following command:

```
pip install -r requirements.txt
```

## Configuration
Make a INI file (for example `settings.ini`) containing configuration for various social platforms. In this section, the configuration is explained for the social platforms.
The INI file contains sections (in between rectangular brackets) and these sections contain key-value pairs. As an example, consider the next INI file:

```
[twitter]
consumer_key=INSERT_CONSUMER_KEY_HERE
consumer_secret=INSERT_CONSUMER_SECRET_HERE
access_token=INSERT_ACCESS_TOKEN_HERE
access_token_secret=INSERT_ACCESS_TOKEN_SECRET_HERE

[facebook]
username=kevin91nl
```

This file contains two sections (namely `twitter` and `facebook`) and the `username` key in the `facebook` section has a corresponding value of `kevin91nl`.

### Twitter
Make a `twitter` section with the following parameters:
- `consumer_key`: The consumer key for the Twitter API.
- `consumer_secret`: The consumer secret for the Twitter API.
- `access_token`: The access token for the Twitter API.
- `access_token_secret`: The access token secret for the Twitter API.

The structure should look like the following:

## Usage

### Twitter
First, specify the configuration INI file. The second argument is the path to the file in which the output of the script is stored. This argument is followed by an action and corresponding arguments. Example usage:

```
python twitter.py settings.ini data/tweets.csv fetch_by_ids data/twitter.txt
```

#### Action fetch_by_ids
This action fetches Tweets using a list of Tweet identifiers. Example usage:

```
python twitter.py settings.ini data/tweets.csv fetch_by_ids data/ids.txt
```

With the following content for `data/ids.txt`:

```
2017-02-28T12:07:16.000+01:00	836533221454131200	801374496548589569
2017-02-28T06:07:16.000+01:00	836442621753114624	801374496548589569
2017-02-11T17:54:13.000+01:00	830459940259164163	801374496548589569
2017-02-11T04:36:23.000+01:00	830259157282480128	801374496548589569
2017-02-16T22:40:01.000+01:00	832343804799832064	3111247474
```

#### Action fetch_by_users
This action fetches Tweets by specifying a file containing Twitter usernames per line. Example usage:

```
python twitter.py settings.ini data/tweets.csv fetch_by_users data/users.txt
```

With the following content for `data/users.txt`:

```
APechtold
geertwilderspvv
```

#### Options

The following options can be set:

 - `delimiter`: The delimiter used in the output CSV file. Example usage: `python twitter.py settings.ini data/tweets.csv fetch_by_users data/users.txt --delimiter ,`. The default delimiter is `\t`.