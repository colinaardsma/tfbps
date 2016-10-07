import webapp2
import urllib2

import sys
sys.path.insert(0, 'libs')
from BeautifulSoup import BeautifulSoup
# import requests

URL = "http://www.fantasypros.com/mlb/projections/hitters.php"


class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = urllib2.urlopen(URL).read()

        soup = BeautifulSoup(content)

        players = []

        for td in soup.findAll('td')[1:]:
            players.append(td)
            # for td in soup.finAll('td'):
            #     players.append(tr)

        self.response.write(players)




app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
