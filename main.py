import webapp2, urllib2, re, sys

sys.path.insert(0, 'libs')
from BeautifulSoup import BeautifulSoup

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #this will only work for fantasypros.com
        URL = "http://www.fantasypros.com/mlb/projections/hitters.php" #currently does not work with https

        content = urllib2.urlopen(URL).read() #convert url to readable html content

        soup = BeautifulSoup(content) #convert html content to searchable BS object

        players = [] #create empty list to hold player data

        trSoup = soup.findAll('tr',attrs={'class':'mpb-available'}) #split data by tr tag with class="mpb-available"

        for tr in trSoup: #iterate over each tr tag in trSoup
            for td in tr.findAll('td'): #iterate over each td tag in tr
                [a.extract() for a in td('a',attrs={'href':'#'})] #remove all <a href="#"></a> tags and their contents
                [small.extract() for small in td('small',attrs={'class':'dl tip'})] #remove all <small class="dl tip"></small> tags and their contents
                [name.replaceWith(name.renderContents() + ",") for name in td('a',attrs={'class':'player-name'})] #remove all <a class="player-name"></a> tags but keep their contents and add a ","
                [team.replaceWith(team.renderContents() + ",") for team in td('a')] #remove all <a></a> tags but keep their contents and add a ","
                players.append(td) #add td to players list

        #need to get all of this into a dictionary instead of a list so that i can easily push it into a db
        #use regular expressions to fix team/position (maybe also ", "?)

        self.response.write(players)




app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
