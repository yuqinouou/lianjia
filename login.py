import json
import requests
import os
import time

def _saveCookie(session, cookieFile):
    with open(cookieFile, "w") as output:
        cookies = session.cookies.get_dict()
        json.dump(cookies, output)
        print("=" * 50)
        print("create cookie:", cookieFile)
        print(cookies)
        print("=" * 50)

def _loadCookie(cookieFile):
    if os.path.exists(cookieFile):
        # print("=" * 50)
        # print("loading cookie:", cookieFile)
        with open(cookieFile, "r") as f:
            cookie = json.load(f)
            # print(cookie)
            return cookie
        # print("=" * 50)
    return None

def _openURL(url, session, delay=0, timeout=10):
    if delay:
        time.sleep(delay)
    return session.get(url, timeout=timeout)
