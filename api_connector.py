"""API Connecting and OAUTH\n
Functions:\n
    request_auth()\n
"""
import json
import urllib2
import urllib
import webbrowser
import base64

# https://developer.yahoo.com/oauth2/guide/flows_authcode/

# consumer key
CLIENT_ID = "dj0yJmk9NWtiV1dqTXlQdU1hJmQ9WVdrOVpIQTNjV1ZCTjJrbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD05ZQ--"
# consumer secret
CLIENT_SECRET = "1e6283bc8ce110e5337aba544561a9d195f526fc"
# REDIRECT_URI = "localhost:8080/redirect/"
REDIRECT_URI = "oob"
AUTHORIZATION_CODE = "wtcdk3w"

def request_auth():
    """Requst Authorication from Yahoo!\n
    https://developer.yahoo.com/oauth2/guide/flows_authcode/#step-2-get-an-authorization-url-and-authorize-access\n
    Args:\n
        url: None.\n
    Returns:\n
        url to Yahoo! for authorization.\n
        Yahoo! will provide a code for entry in the next step.\n
    Raises:\n
        None.
    """
    url = 'https://api.login.yahoo.com/oauth2/request_auth'
    parameters = urllib.urlencode({
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code'
        })
    url += '?' + parameters
    request = urllib2.Request(url)
    content = urllib2.urlopen(request)
    return content.url
# 'qguvnhp'

def get_token(authorization_code):
    url = 'https://api.login.yahoo.com/oauth2/get_token'
    auth_string = "{}:{}".format(CLIENT_ID, CLIENT_SECRET)
    auth_header = base64.b64encode(auth_string)
    # auth_header = 'ZGoweUptazlOV3RpVjFkcVRYbFFkVTFoSm1ROVdWZHJPVnBJUVROalYxWkNUakpyYldOSGJ6bE5RUzB0Sm5NOVkyOXVjM1Z0WlhKelpXTnlaWFFtZUQwNVpRLS06MWU2MjgzYmM4Y2UxMTBlNTMzN2FiYTU0NDU2MWE5ZDE5NWY1MjZmYw=='
    # body = "grant_type=authorization_code&redirect_uri=oob&code=************"
    headers = {
        'Authorization': 'Basic ' + auth_header,
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    body = urllib.urlencode({
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': authorization_code
        })
    # url += '?' + body
    request = urllib2.Request(url, data=body, headers=headers)
    # request.headers = headers
    # request.body = body
    content = urllib2.urlopen(request)
    # return content.url
    return content.read()

# webbrowser.open(request_auth())
print get_token(AUTHORIZATION_CODE)

# def test():
#     flow = oath2client.OAuth2WebServerFlow(client_id=CONSUMER_KEY,
#                                            client_secret=CONSUMER_SECRET,
#                                            scope='https://www.googleapis.com/auth/calendar',
#                                            redirect_uri='http://example.com/auth_return')
#     flow = flow
