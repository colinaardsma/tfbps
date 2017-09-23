"""API Connecting and OAUTH\n
Functions:\n
    request_auth()\n
"""
import json
import urllib2
import urllib
import webbrowser
import base64
import HTMLParser
import datetime
import db_models

# https://developer.yahoo.com/oauth2/guide/flows_authcode/

"""TESTING"""
# consumer key
CLIENT_ID = "dj0yJmk9cEQyTkhmUUt5ekN5JmQ9WVdrOWFtRkdUSHB0Tm1zbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0yYQ--"
# consumer secret
CLIENT_SECRET = "2fdb054293ed5c071e62048411c9f3f204512bcc"
REDIRECT_URI = "http://grays-sports-almanac.appspot.com"

"""PRODUCTION"""
# consumer key
# CLIENT_ID = "dj0yJmk9YWE1SnlhV0lUbndoJmQ9WVdrOU9FUmhUelV6TkdVbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1lMQ--"
# consumer secret
# CLIENT_SECRET = "55d6606ea0bec9a1468d3ea01bbf1c9991dbf93f"
# REDIRECT_URI = "oob"

def request_auth(redirect_path):
    """Requst Authorication from Yahoo!\n
    https://developer.yahoo.com/oauth2/guide/flows_authcode/#step-2-get-an-authorization-url-and-authorize-access\n
    Args:\n
        None.\n
    Returns:\n
        url to Yahoo! for authorization.\n
        Yahoo! will provide a code for entry in the next step.\n
    Raises:\n
        None.
    """
    url = 'https://api.login.yahoo.com/oauth2/request_auth'
    parameters = urllib.urlencode({
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI + redirect_path,
        'response_type': 'code'
        })
    url += '?' + parameters
    request = urllib2.Request(url)
    content = urllib2.urlopen(request)
    return content.url

def get_token(authorization_code, redirect_path):
    """Requst Token from Yahoo!\n
    https://developer.yahoo.com/oauth2/guide/flows_authcode/#step-4-exchange-authorization-code-for-access-token\n
    Args:\n
        authorization_code: Code provided by Yahoo! in request_auth() method.\n
    Returns:\n
        access_token, token_type, expires_in, refresh_token, xoauth_yahoo_guid in json form.\n
    Raises:\n
        None.
    """
    url = 'https://api.login.yahoo.com/oauth2/get_token'
    auth_string = "{}:{}".format(CLIENT_ID, CLIENT_SECRET)
    auth_header = base64.b64encode(auth_string)
    headers = {
        'Authorization': 'Basic ' + auth_header,
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    body = urllib.urlencode({
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI + redirect_path,
        'code': authorization_code
        })
    request = urllib2.Request(url, data=body, headers=headers)
    content = urllib2.urlopen(request)
    raw_json = content.read()
    return raw_json

def yql_query(path, oauth_token):
    """YQL call to Yahoo! API\n
    Actually an alternative to the YQL call done through a URL.
    Args:\n
        path: YQL call translated to URL Path.\n
        oauth_token: json OAuth token returned in get_token().\n
    Returns:\n
        YQL data in XML format.\n
    Raises:\n
        None.
    """
    baseurl = "https://fantasysports.yahooapis.com/fantasy/v2"
    url = baseurl + path
    raw_json = get_json_data(url, oauth_token)
    return raw_json

def get_guid(oauth_token):
    url = "https://social.yahooapis.com/v1/me/guid"
    raw_json = get_json_data(url, oauth_token)
    return raw_json

def get_json_data(url, oauth_token):
    url = url + "?format=json"
    raw_json = get_xml_data(url, oauth_token)
    return raw_json

def get_xml_data(url, oauth_token):
    headers = {'Authorization': str(oauth_token['token_type']).capitalize() +
                                " " + str(oauth_token['access_token'])}
    request = urllib2.Request(url, headers=headers)
    content = urllib2.urlopen(request)
    raw_xml = content.read()
    return raw_xml

def check_token_expiration(user, redirect_path):
    """Check if Token is expired and if so refresh from Yahoo!\n
    https://developer.yahoo.com/oauth2/guide/flows_authcode/#step-4-exchange-authorization-code-for-access-token\n
    Args:\n
        user: The User DB model.\n
    Returns:\n
        access_token, token_type, expires_in, refresh_token, xoauth_yahoo_guid in json form.\n
    Raises:\n
        None.
    """
    # if (user.token_expiration - datetime.datetime.now()).total_seconds() > 240:
    #     return
    url = 'https://api.login.yahoo.com/oauth2/get_token'
    auth_string = "{}:{}".format(CLIENT_ID, CLIENT_SECRET)
    auth_header = base64.b64encode(auth_string)
    headers = {
        'Authorization': 'Basic ' + auth_header,
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    body = urllib.urlencode({
        'grant_type': 'refresh_token',
        'redirect_uri': REDIRECT_URI + redirect_path,
        'refresh_token': user.refresh_token
        })
    print "**************"
    print "Refresh_token: " + user.refresh_token
    request = urllib2.Request(url, data=body, headers=headers)
    content = urllib2.urlopen(request)
    raw_json = content.read()
    token_dict = json.loads(raw_json)
    token_expiration = (datetime.datetime.now() +
                        datetime.timedelta(seconds=token_dict['expires_in']))
    user.access_token = token_dict['access_token']
    user.token_expiration = token_expiration
    user.refresh_token = token_dict['refresh_token']
    db_models.update_user(user)
    return token_dict
