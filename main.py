import webapp2 #built in python classes
import dbmodels, fPP #custom python classes

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #this will only work for fantasypros.com
        URL = "http://www.fantasypros.com/mlb/projections/hitters.php" #currently does not work with https

        players = fPP.pullData(URL)

        self.response.write(players)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
