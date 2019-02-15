from re import compile
from os import environ
from requests import get, post
import time

_users = compile(r"(<@)([\w]+)([>|])")


def list_users(event):
    if "text" not in event:
        return []
    lst = []
    for user in _users.finditer(event["text"]):
        lst.append(user.group(2))
    return lst


def get_week(season):
    if season:
        sunday = time.time() - (time.time() % 604800) - 280000
        return int((sunday-season["start_ts"])//604800)
    else:
        return 0


def get_channel(channel):
    return '#' + get('https://slack.com/api/channels.info', {
        'channel': channel,
        'token': environ['OAUTH_TOKEN']
    }).json()['channel']['name']


def get_permalink(channel, ts):
    json = get('https://slack.com/api/chat.getPermalink', {
        'channel': channel,
        'message_ts': ts,
        'token': environ['OAUTH_TOKEN']
    }).json()
    if "permalink" in json:
        return json['permalink']
    else:
        return "Link not found."


def react(channel, timestamp, reaction):
    post('https://slack.com/api/reactions.add', {
        'channel': channel,
        'name': reaction,
        'timestamp': timestamp,
        'token': environ['OAUTH_TOKEN']
    })
