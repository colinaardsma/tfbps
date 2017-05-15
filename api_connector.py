"""API Connecting and OAUTH"""
import json
# import oath2client
import urllib2
import urllib
import requests
import webbrowser
# import requests_toolbelt.adapters.appengine
# from api import urlfetch
# urlfetch.set_default_fetch_deadline(45)
# requests_toolbelt.adapters.appengine.monkeypatch()
# https://developer.yahoo.com/oauth2/guide/flows_authcode/

CLIENT_ID = "dj0yJmk9NWtiV1dqTXlQdU1hJmQ9WVdrOVpIQTNjV1ZCTjJrbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD05ZQ--"
CLIENT_SECRET = "1e6283bc8ce110e5337aba544561a9d195f526fc"
REDIRECT_URI = "localhost:8080/redirect"
# REDIRECT_URI = "oob"

def request_auth():
    url = 'https://api.login.yahoo.com/oauth2/request_auth?'
    body = urllib.urlencode({
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code'
        })
    content = urllib2.urlopen(url=url, data=body)
    return content.url

def get_token():
    url = 'https://api.login.yahoo.com/oauth2/request_auth?'
    # body = "grant_type=authorization_code&redirect_uri=oob&code=************"
    body = {
        'grant_type': 'authorization_code',
        'redirect_uri': 'oob',
        'code': '************',
        }
    headers = {
        'Authorization': 'Basic **************',
        'Content-Type': 'application/json'
        }

    r = requests.post(url, data=body, headers=headers)

webbrowser.open(request_auth())

# def test():
#     flow = oath2client.OAuth2WebServerFlow(client_id=CONSUMER_KEY,
#                                            client_secret=CONSUMER_SECRET,
#                                            scope='https://www.googleapis.com/auth/calendar',
#                                            redirect_uri='http://example.com/auth_return')
#     flow = flow
