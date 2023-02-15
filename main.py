# blipsCLI
# by venturingfan/suspecting (https://github.com/suspecting)
# with help from the Python Discord

import requests
import argparse
import feedparser
import re

parser = argparse.ArgumentParser(prog = 'blipsCLI', description='Blips from your command line.')
parser.add_argument("-u", "--update", help="Sends update to Blips.")
parser.add_argument('-d','--direct', nargs='+', help='Sends Direct Message to Blips user.')
parser.add_argument('-f', '--feed', action='store_true', help='Shows last 10 statuses.')
parser.add_argument('-s', '--star', help='Star/Favorite a status by status number.')
parser.add_argument('-p', '--profile', help='View a profile.')
parser.add_argument('-b', '--block', help='Block a profile.')
args = parser.parse_args()

print(args)

SigninUrl = 'https://blips.club/signin'
StatusUrl = 'https://blips.club/status/create'
DirectUrl = 'https://blips.club/direct_messages/create'
FavoriteUrl = 'https://blips.club/favorites/create'

f = open("user.txt", "r")
UserInfo = f.read().split(", ")

AuthPayload = { # used for authentication
    'username': UserInfo[0],
    'password': UserInfo[1]
}

session = requests.session()
resp = session.get(SigninUrl) 
cookie_session = resp.cookies['PHPSESSID']
AuthResponse = session.post(SigninUrl, data=AuthPayload)


if args.update:
    UpdatePayload = {
        'session': cookie_session,
        'status': args.update, 
    }
    if len(args.debug) >= 140:
        print("Woah there. Condense what you just said (More than 140 characters) and then come back.")
    else:
        UpdateResponse = session.post(StatusUrl, data=UpdatePayload)
        print("Update sent.")
    
if args.direct:
    DirectPayload = {
        'session': cookie_session,
        'status': args.direct[1],
        'recipient': args.direct[0]
    }
    if len(args.debug) >= 140:
        print("Woah there. Condense what you just said (More than 140 characters) and then come back.")
    else:
        DirectResponse = session.post(DirectUrl, data=DirectPayload)
        print("Message sent to " + args.direct[0])

if args.feed:
    Feed = feedparser.parse("https://blips.club/" + AuthPayload['username'] + "/with_friends.rss")
    for i in range(10):
        PostId = re.sub('\D', '', Feed.entries[i].link)
        print(Feed.entries[i].title + " / Status #" + PostId)

if args.star:
    FavoritePayload = {
        'session': cookie_session,
        'id': args.star,
    }
    
    FavoriteResponse = session.post(FavoriteUrl, data=FavoritePayload)

if args.profile:
    Feed = feedparser.parse("https://blips.club/" + args.profile + "/feed.rss")
    for i in range(10):
        PostId = re.sub('\D', '', Feed.entries[i].link)
        print(Feed.entries[i].title + " / Status #" + PostId)
        
if args.block:
    print("Not yet.")