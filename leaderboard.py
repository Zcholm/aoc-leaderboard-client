#!/usr/bin/python3
import json
#import urllib
from argparse import ArgumentParser as AP
import requests
import sqlite3
import http.cookiejar as cookielib

def get_json(json_id, cookie):
    json_url = "https://adventofcode.com/2020/leaderboard/private/view/{0}.json".format(json_id)

    s = requests.Session()
    s.cookies = cookie
    return json.loads(s.get(json_url).text)

def has_cookie(cj, url):
    for c in cj:
        if url in cj:
            return True
    return False

# Shamelessly stolen (https://stackoverflow.com/questions/49502254/how-to-import-firefox-cookies-to-python-requests):
def get_cookies(cj, ff_cookies):
    con = sqlite3.connect(ff_cookies)
    cur = con.cursor()
    cur.execute("SELECT host, path, isSecure, expiry, name, value FROM moz_cookies")
    for item in cur.fetchall():
        if "adventofcode.com" in item[0]:
            c = cookielib.Cookie(0, item[4], item[5],
                None, False,
                item[0], item[0].startswith('.'), item[0].startswith('.'),
                item[1], False,
                item[2],
                item[3], item[3]=="",
                None, None, {})
            cj.set_cookie(c)


def parse_json(data):
    # TODO
    return

def main():
    parser = AP(description="Create a human friendly representation of an AdventOfCode leaderboard")
    parser.add_argument("--id", type=int)
    parser.add_argument("--cookies")

    args = parser.parse_args()

    cj = cookielib.CookieJar()

    ff_cookies = "cookies.sqlite"


    if args.id is not None and args.cookies is not None:
        get_cookies(cj, args.cookies)
        json_data = get_json(args.id, cj).read()
    else:
        with open("input.json") as j:
            json_data = json.loads(j.read())


    parse_json(json_data)


if __name__ == "__main__":
    main()

