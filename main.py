import webapp2, urllib2, re, sys #built in python classes
import dbmodels #custom python classes

sys.path.insert(0, 'libs')
from BeautifulSoup import BeautifulSoup, Tag

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #this will only work for fantasypros.com
        URL = "http://www.fantasypros.com/mlb/projections/hitters.php" #currently does not work with https

        content = urllib2.urlopen(URL).read() #convert url to readable html content

        soup = BeautifulSoup(content) #convert html content to searchable BS object

        # for a in soup.select('a'):
        #     # insert sup tag after the span
        #     td = soup.new_tag('td')
        #     td.string = a
        #     a.insert_after(td)
        #
        #     # replace the span tag with it's contents
        #     a.unwrap()


        #.wrap(soup.new_tag("b")) need to wrap player name, pos, team

        players = [] #create empty list to hold player data

        trSoup = soup.findAll('tr',attrs={'class':'mpb-available'}) #split data by tr tag with class="mpb-available"; stats per player

        for tr in trSoup: #iterate over each tr tag in trSoup
            for td in tr.findAll('td'): #iterate over each td tag in tr; break columns apart
                [a.extract() for a in td('a',attrs={'href':'#'})] #remove all <a href="#"></a> tags and their contents; empty tag
                [small.extract() for small in td('small',attrs={'class':'dl tip'})] #remove all <small class="dl tip"></small> tags and their contents; DL status
                [name.replaceWith(name.renderContents() + ",") for name in td('a',attrs={'class':'player-name'})] #remove all <a class="player-name"></a> tags but keep their contents and add a ","; player name
                [name.findAll('a',attrs={'class':'player-name'})] #remove all <a class="player-name"></a> tags but keep their contents and add a ","; player name

                [team.replaceWith(team.renderContents()) for team in td('a')] #remove all <a></a> tags but keep their contents and add a ","; team name
                [teamPos.replaceWith(teamPos.renderContents().replace(",", "/").replace("(", "").replace(")","").replace(" - ", ",")) for teamPos in td('small')] #remove all <small></small> tags but keep their contents, change "," to "/", change "(" to "", change ")" to "", change " - " to ",",; team and position
                [div.extract() for div in td('div',attrs={'id':'directions_extension'})] #remove all <div id="directions-extension"></div> tags and their contents; empty div tag
                players.append(td) #add td to players list

        # players = [i.split(',')[0] for i in players]
        # pl = [players[x:x+20] for x in range(0, len(players), 20)]

        # player = dbmodels.fantProProj(name=name, team=team, pos=pos, ab=ab, r=r, hr=hr, rbi=rbi, sb=sb, avg=avg, obp=obp, h=h, double=double, triple=triple, bb=bb, k=k, slg=slg, ops=ops)


        #need to get all of this into a dictionary instead of a list so that i can easily push it into a db
        #use regular expressions to fix team/position (maybe also ", "?)

        self.response.write(players)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
