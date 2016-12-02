import requests
import os
import sys
import json
from bs4 import BeautifulSoup as BS
from bs4 import SoupStrainer as SS

import login
import db
import spider

# load constants
from constants import *
# load username and password
from password import *

# check if cookie exists, if not create cookie
# create new session
session = requests.session()
# session.headers = headers # header is redundent

# initialize session.cookie
res = session.post(homeURL)
login._saveCookie(session, cookieFile)
# cookie = _loadCookie(cookieFile)

# get info for login form. only lt is necessary
loginhtml = login._openURL(loginURL, session).text
ltlogin = BS(loginhtml, "html.parser").find("input", {"name":"lt"})["value"]
execution = BS(loginhtml, "html.parser").find("input", {"name":"execution"})["value"]
_eventId = BS(loginhtml, "html.parser").find("input", {"name":"_eventId"})["value"]
# print(ltlogin)
# print(execution)
# print(_eventId)

# some more info, not used
# jsession = re.search(r'jsessionid=[0-9A-Za-z\-]*', BS(loginhtml, "html.parser").find("form")["action"]).group(0)
# print(jsession)
# ticketfinder = SS('script', src=re.compile('v=[0-9]+$'))
# tag = [tag for tag in BS(html, "html.parser", parse_only=ticketfinder)][1]
# ticketno = re.search("[0-9]+$", tag['src']).group(0)
# print(ticketno)
# lthtml = _openURL(ltURL + ticketno, session).text
# ltquery = eval(BS(lthtml, "html.parser").text)['data']
# print(ltquery)

# create form
data = {
    'username': username,
    'password': password,
    'execution': execution,
    '_eventId': _eventId,
    'lt': ltlogin,
    'verifyCode': '',
    'redirect': ''
}

# resubmit form to login
res = session.post(loginURL, data=data)
login._saveCookie(session, cookieFile)
# cookie = _loadCookie(cookieFile)

nHouse = BS(login._openURL(targetURL, session).text, "html.parser").find("h2").span.text
print("Total Number of Recs:", nHouse)
