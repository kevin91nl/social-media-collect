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
First, specify the configuration INI file. Then, specify the path to the file containing Tweet IDs. The last argument is the path to the file in which the output of the script is stored. Example usage:

```
python twitter.py settings.ini data/twitter.txt data/tweets.csv
```