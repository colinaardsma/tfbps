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

# https://developer.yahoo.com/oauth2/guide/flows_authcode/

"""TESTING"""
# consumer key
CLIENT_ID = "dj0yJmk9cEQyTkhmUUt5ekN5JmQ9WVdrOWFtRkdUSHB0Tm1zbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0yYQ--"
# consumer secret
CLIENT_SECRET = "2fdb054293ed5c071e62048411c9f3f204512bcc"
REDIRECT_URI = "http://grays-sports-almanac.appspot.com/localhostredirect"

"""PRODUCTION"""
# consumer key
# CLIENT_ID = "dj0yJmk9YWE1SnlhV0lUbndoJmQ9WVdrOU9FUmhUelV6TkdVbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1lMQ--"
# consumer secret
# CLIENT_SECRET = "55d6606ea0bec9a1468d3ea01bbf1c9991dbf93f"
# REDIRECT_URI = "oob"

def request_auth():
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
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code'
        })
    url += '?' + parameters
    request = urllib2.Request(url)
    content = urllib2.urlopen(request)
    return content.url

def get_token(authorization_code):
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
        'redirect_uri': REDIRECT_URI,
        'code': authorization_code
        })
    request = urllib2.Request(url, data=body, headers=headers)
    content = urllib2.urlopen(request)
    return json.loads(content.read())

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


# AUTHORIZATION_CODE = "yn2dxse"
# LEAGUE_YEAR_CODE = "370"
# LEAGUE_KEY = "5091"
# PATH = "/leagues;league_keys=" + LEAGUE_YEAR_CODE + ".l." + LEAGUE_KEY + "/standings"
# # webbrowser.open(request_auth())
# OAUTH_TOKEN = {u'access_token': u'aJZ7CI3OogsRi3YeufErdSjuw0MRG3r6ZtMAlptP80EfUUBr31Jqn.d1ikQA0goSrGD.9soz5MlKQ3FFhgVjEXhirRN.2XbrS4X.BM1J0DkwU7ElcEZZEyWvk8mMXfe47BslXzkmPIEMSoqe11Z39Lr5HE6NH5ifMv5TuK9jSg4HWnlUtaeD6ImqxGN9AAzqlCFsael_PfRNhhscNi9XEowp4s2ljogW.AIqubD8zRI3ZX7HwkeV0VqBGr2S8riSOjQMNN68xSyLTuOm1qbuJBGegVh6dZDZdrc5X6vxG5W6gpSGyZROtG8G_RE8ByALiwryMEpa7yL9L1S_j5GP2U0vHnbSLq7LKNl459FqI4nGOi83WGPUxvvRThCLysq5OVPPmgOojJbWbvFdkIyTx88rdjoYJEVLDlk7tjGn58K8TwuQbsrV1S3fsveRSzs3d.gee0k3cs3QniTNd5ibvw13bO0lrfrGZ.VWShJ0hkgAJ5tVLz6JaaZMnNmishUQEqMEUwA24daGrCiuFpJZoie38do.vvlXlASJY0m1Ds2i9MYVE57dpfJMTkalDpo_REzTXqMmcIlANGsWibbHLfEdLWAQlrbVwl_T.zfBARlX1A1pz0X0zDKw9fHnEovGlgXYCBL3uuxo.Xt_1qaJ6j4Kn89gJ.KTVHcDVYCaZOj3uHkd.kpfOOqTJNL0D2rbXFpoJ2Aixr4qGnK_THgVWiHmQcbKxtlL.nGPjvwx2wiN6wPKJYFTL1vf2i5hDdicbmu5_qBsq_TVNNmgDHfL4fESGzBgq77HyTI6mebFfBt9owqZudA6srbBNrmFDzAz.VPLsf.KJuIL01zK5rhaWF3cc7tp0a6.bCE6.V6oCckA3y_mJB4pxQmeRUxfc0c8kCaxpx6EjPRRA.2X6F4kdmcD5Wku4R0jz7dqGR1_m7wa.9qMo7G7TrT67xN3umVpSsBaoqkmxxqw6G7wL0egQR7dwyyn2aJWQ81hfLTMwBasmqr94HcfuQCA3tcyYeemm9AaZg2kNXqMgPq51pnA1892p2Spf17W3gFQlK_fu_7xl4LguBJi8H5.Kw--', u'token_type': u'bearer', u'expires_in': 3600, u'xoauth_yahoo_guid': u'PP5K6WYOIYQL4ZWJAYTN2ZQ5CU', u'refresh_token': u'ACRar1mAeCTt7i0dv3kIcSwD4yECKpGzipn4E2f1RrSZJmJecQ--'}
# # print get_token(AUTHORIZATION_CODE)
# print yql_query(PATH, OAUTH_TOKEN).replace(r"\/", "/")
# # print json_return
