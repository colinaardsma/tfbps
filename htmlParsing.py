import webapp2, urllib2, re, sys, itertools #built in python classes
import dbmodels #custom python classes
import string

sys.path.insert(0, 'libs')
from BeautifulSoup import BeautifulSoup, Tag

def fppDataPull(url):
    content = urllib2.urlopen(url).read() #convert url to readable html content

    soup = BeautifulSoup(content) #convert html content to searchable BS object

    playerSoap = [] #create empty list to hold player data

    trSoup = soup.findAll('tr',attrs={'class':'mpb-available'}) #split data by tr tag with class="mpb-available"; stats per player

    for tr in trSoup: #iterate over each tr tag in trSoup
        for td in tr.findAll('td'): #iterate over each td tag in tr; break columns apart
            [a.extract() for a in td('a',attrs={'href':'#'})] #remove all <a href="#"></a> tags and their contents; empty tag
            [small.extract() for small in td('small',attrs={'class':'dl tip'})] #remove all <small class="dl tip"></small> tags and their contents; DL status
            [name.replaceWith(name.renderContents() + ", ") for name in td('a',attrs={'class':'player-name'})] #remove all <a class="player-name"></a> tags but keep their contents and add a ","; player name
            [team.replaceWith(team.renderContents()) for team in td('a')] #remove all <a></a> tags but keep their contents and add a ","; team name
            [teamPos.replaceWith(teamPos.renderContents().replace(",", "/").replace("(", "").replace(")","").replace(" - ", ", ")) for teamPos in td('small')] #remove all <small></small> tags but keep their contents, change "," to "/", change "(" to "", change ")" to "", change " - " to ", ",; team and position
            # [div.extract() for div in td('div',attrs={'id':'directions_extension'})] #remove all <div id="directions-extension"></div> tags and their contents; empty div tag
            tagless = td.getText() #remove all remaining tags
            playerSoap.append(tagless) #add td to playerSoap list

    playerSoap = [pl.split(",") for pl in playerSoap] #split playerSoap data into a list (this makes a list of lists)
    playerList = list(itertools.chain.from_iterable(playerSoap)) #covert list of lists into single list
    # [pl.lstrip() for pl in playerList]

    #need to calculate per league history (past 3 years?)
    sgpMultR = 24.6
    sgpMultHR = 10.4
    sgpMultRBI = 24.6
    sgpMultSB = 9.4
    sgpMultOPS = 0.0024

    for i in range(0, len(playerSoap), 20): #assign each piece of data to a variable (17 pieces of usable data, 18-20 are ownership %s)
        name = playerList[i]
        team = playerList[i + 1]
        pos = playerList[i + 2]
        ab = int(playerList[i + 3])
        r = int(playerList[i + 4])
        hr = int(playerList[i + 5])
        rbi = int(playerList[i + 6])
        sb = int(playerList[i + 7])
        avg = float(playerList[i + 8])
        obp = float(playerList[i + 9])
        h = int(playerList[i + 10])
        double = int(playerList[i + 11])
        triple = int(playerList[i + 12])
        bb = int(playerList[i + 13])
        k = int(playerList[i + 14])
        slg = float(playerList[i + 15])
        ops = float(playerList[i + 16])

        player = dbmodels.fantProProjB(name=name, team=team, pos=pos, ab=ab, r=r, hr=hr, rbi=rbi, sb=sb, avg=avg, obp=obp, h=h, double=double, triple=triple, bb=bb, k=k, slg=slg, ops=ops) #convert data into db object
        #calculate sgp value and add to db object
        player.sgp = (player.r/sgpMultR)+(player.hr/sgpMultHR)+(player.rbi/sgpMultRBI)+(player.sb/sgpMultSB)+((((((player.obp*(player.ab*1.15))+2178.8)/((player.ab*1.15)+6682))+(((player.slg*player.ab)+2528.5)/(player.ab+5993)))-0.748)/sgpMultOPS)
        player.put() #store player db object in database


    # name = [playerList[x] for x in range(0, len(playerSoap), 20)]
    # team = [playerList[x] for x in range(1, len(playerSoap), 20)]
    # pos = [playerList[x] for x in range(2, len(playerSoap), 20)]
    # ab = [int(playerList[x]) for x in range(3, len(playerSoap), 20)]
    # r = [int(playerList[x]) for x in range(4, len(playerSoap), 20)]
    # hr = [int(playerList[x]) for x in range(5, len(playerSoap), 20)]
    # rbi = [int(playerList[x]) for x in range(6, len(playerSoap), 20)]
    # sb = [int(playerList[x]) for x in range(7, len(playerSoap), 20)]
    # avg = [float(playerList[x]) for x in range(8, len(playerSoap), 20)]
    # obp = [float(playerList[x]) for x in range(9, len(playerSoap), 20)]
    # h = [int(playerList[x]) for x in range(10, len(playerSoap), 20)]
    # double = [int(playerList[x]) for x in range(11, len(playerSoap), 20)]
    # triple = [int(playerList[x]) for x in range(12, len(playerSoap), 20)]
    # bb = [int(playerList[x]) for x in range(13, len(playerSoap), 20)]
    # k = [int(playerList[x]) for x in range(14, len(playerSoap), 20)]
    # slg = [float(playerList[x]) for x in range(15, len(playerSoap), 20)]
    # ops = [float(playerList[x]) for x in range(16, len(playerSoap), 20)]
    #
    # player = dbmodels.fantProProjB(name=name, team=team, pos=pos, ab=ab, r=r, hr=hr, rbi=rbi, sb=sb, avg=avg, obp=obp, h=h, double=double, triple=triple, bb=bb, k=k, slg=slg, ops=ops)


    #need to get all of this into a dictionary instead of a list so that i can easily push it into a db
    #use regular expressions to fix team/position (maybe also ", "?)

    # return playerList
