import webapp2, urllib2, re, sys, itertools #built in python classes
import dbmodels #custom python classes
import string

sys.path.insert(0, 'libs')
from BeautifulSoup import BeautifulSoup, Tag

def pullData(url):
    content = urllib2.urlopen(url).read() #convert url to readable html content

    soup = BeautifulSoup(content) #convert html content to searchable BS object

    players = [] #create empty list to hold player data

    trSoup = soup.findAll('tr',attrs={'class':'mpb-available'}) #split data by tr tag with class="mpb-available"; stats per player

    for tr in trSoup: #iterate over each tr tag in trSoup
        for td in tr.findAll('td'): #iterate over each td tag in tr; break columns apart
            [a.extract() for a in td('a',attrs={'href':'#'})] #remove all <a href="#"></a> tags and their contents; empty tag
            [small.extract() for small in td('small',attrs={'class':'dl tip'})] #remove all <small class="dl tip"></small> tags and their contents; DL status
            [name.replaceWith(name.renderContents() + ", ") for name in td('a',attrs={'class':'player-name'})] #remove all <a class="player-name"></a> tags but keep their contents and add a ","; player name
            # [name.findAll('a',attrs={'class':'player-name'})] #remove all <a class="player-name"></a> tags but keep their contents and add a ","; player name

            [team.replaceWith(team.renderContents()) for team in td('a')] #remove all <a></a> tags but keep their contents and add a ","; team name
            [teamPos.replaceWith(teamPos.renderContents().replace(",", "/").replace("(", "").replace(")","").replace(" - ", ", ")) for teamPos in td('small')] #remove all <small></small> tags but keep their contents, change "," to "/", change "(" to "", change ")" to "", change " - " to ",",; team and position
            # [div.extract() for div in td('div',attrs={'id':'directions_extension'})] #remove all <div id="directions-extension"></div> tags and their contents; empty div tag
            tagless = td.getText()
            players.append(tagless) #add td to players list

    # pl = [players[x:x+20] for x in range(0, len(players), 20)]

    # players = str(players[0:len(players)]).split(", ")
    # players = [pl.replace("[", "").replace("]", "") for pl in players]
    # playerList = []
    players = [pl.split(",") for pl in players]
    playerList = list(itertools.chain.from_iterable(players))
    [pl.lstrip() for pl in playerList]

    # name = [playerList[x] for x in range(0, len(players), 20)]
    # team = [playerList[x] for x in range(1, len(players), 20)]
    # pos = [playerList[x] for x in range(2, len(players), 20)]
    # ab = [int(playerList[x]) for x in range(3, len(players), 20)]
    # r = [int(playerList[x]) for x in range(4, len(players), 20)]
    # hr = [int(playerList[x]) for x in range(5, len(players), 20)]
    # rbi = [int(playerList[x]) for x in range(6, len(players), 20)]
    # sb = [int(playerList[x]) for x in range(7, len(players), 20)]
    # avg = [float(playerList[x]) for x in range(8, len(players), 20)]
    # obp = [float(playerList[x]) for x in range(9, len(players), 20)]
    # h = [int(playerList[x]) for x in range(10, len(players), 20)]
    # double = [int(playerList[x]) for x in range(11, len(players), 20)]
    # triple = [int(playerList[x]) for x in range(12, len(players), 20)]
    # bb = [int(playerList[x]) for x in range(13, len(players), 20)]
    # k = [int(playerList[x]) for x in range(14, len(players), 20)]
    # slg = [float(playerList[x]) for x in range(15, len(players), 20)]
    # ops = [float(playerList[x]) for x in range(16, len(players), 20)]
    #
    # player = dbmodels.fantProProj(name=name, team=team, pos=pos, ab=ab, r=r, hr=hr, rbi=rbi, sb=sb, avg=avg, obp=obp, h=h, double=double, triple=triple, bb=bb, k=k, slg=slg, ops=ops)


    #need to get all of this into a dictionary instead of a list so that i can easily push it into a db
    #use regular expressions to fix team/position (maybe also ", "?)

    return playerList
