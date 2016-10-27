import webapp2, urllib2, re, sys, itertools #built in python classes
import dbmodels #custom python classes
import string
from google.appengine.ext import db
from google.appengine.api import memcache

sys.path.insert(0, 'libs/BeautifulSoup')
from BeautifulSoup import BeautifulSoup, Tag

def fpprojbdatapull(url):
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

    #need to calculate per league history (past 3 years?)
    sgpMultR = 24.6
    sgpMultHR = 10.4
    sgpMultRBI = 24.6
    sgpMultSB = 9.4
    sgpMultOPS = 0.0024

    #delete all records from database before rebuidling
    if dbmodels.FPProjB:
        remove = dbmodels.FPProjB.all() # .all() = "SELECT *"
        db.delete(remove)

    #flush memcache
    key = "fpprojb" #create key
    memcache.delete(key)

    #need to erase duplicates, are there any?

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
        category = "fpprojb"

        #rebuild database
        player = dbmodels.FPProjB(name=name, team=team, pos=pos, ab=ab, r=r, hr=hr, rbi=rbi, sb=sb, avg=avg, obp=obp, h=h, double=double, triple=triple, bb=bb, k=k, slg=slg, ops=ops, category=category) #convert data into db object
        #calculate sgp value and add to db object
        player.sgp = (player.r/sgpMultR)+(player.hr/sgpMultHR)+(player.rbi/sgpMultRBI)+(player.sb/sgpMultSB)+((((((player.obp*(player.ab*1.15))+2178.8)/((player.ab*1.15)+6682))+(((player.slg*player.ab)+2528.5)/(player.ab+5993)))-0.748)/sgpMultOPS)
        player.put() #store player db object in database

def fpprojpdatapull(url):
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

    #need to calculate per league history (past 3 years?)
    sgpMultW = 3.03
    sgpMultSV = 9.95
    sgpMultK = 39.3
    sgpMultERA = -0.0706
    sgpMultWHIP = -0.015

    #delete all records from database before rebuidling
    if dbmodels.FPProjP:
        remove = dbmodels.FPProjP.all() # .all() = "SELECT *"
        db.delete(remove)

    #flush memcache
    key = "fpprojp" #create key
    memcache.delete(key)

    #need to erase duplicates, are there any?

    for i in range(0, len(playerSoap), 20): #assign each piece of data to a variable (17 pieces of usable data, 18-20 are ownership %s)
        name = playerList[i]
        team = playerList[i + 1]
        pos = playerList[i + 2]
        ip = float(playerList[i + 3])
        k = int(playerList[i + 4])
        w = int(playerList[i + 5])
        sv = int(playerList[i + 6])
        era = float(playerList[i + 7])
        whip = float(playerList[i + 8])
        er = int(playerList[i + 9])
        h = int(playerList[i + 10])
        bb = int(playerList[i + 11])
        hr = int(playerList[i + 12])
        g = int(playerList[i + 13])
        gs = int(playerList[i + 14])
        l = int(playerList[i + 15])
        cg = int(playerList[i + 16])
        category = "fpprojp"

        #rebuild database
        player = dbmodels.FPProjP(name=name, team=team, pos=pos, ip=ip, k=k, w=w, sv=sv, era=era, whip=whip, er=er, h=h, bb=bb, hr=hr, g=g, gs=gs, l=l, cg=cg, category=category) #convert data into db object
        #calculate sgp value and add to db object
        player.sgp = (player.w/sgpMultW)+(player.sv/sgpMultSV)+(player.k/sgpMultK)+(((475+player.era)*9/(1192 + player.ip)-3.59)/sgpMultERA)+(((1466+player.h+player.bb)/(1192+player.ip)-1.23)/sgpMultWHIP)
        player.put() #store player db object in database
