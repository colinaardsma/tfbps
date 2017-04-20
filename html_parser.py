"""HTML Parsing"""
import urllib2
import unicodedata
from lxml import html

def fantasy_pro_players(url):
    """Parse batter data from url"""
    content = urllib2.urlopen(url).read().decode('utf-8')
    content = unicodedata.normalize('NFKD', content).encode('ASCII', 'ignore')
    document = html.document_fromstring(content)
    headings_list_html = document.xpath("//div[@class='mobile-table']" +
                                        "/table/thead/tr/descendant::*/text()")
    headings_list_html[len(headings_list_html) - 1] = "AVG_OWN_PCT"
    headings_list_html.append("YAHOO_OWN_PCT")
    headings_list_html.append("ESPN_OWN_PCT")
    body_html = document.xpath("//div[@class='mobile-table']/table/tbody/tr")
    player_list = []
    for player_html in body_html:
        single_player_html = player_html.xpath("descendant::td")
        player_stats = fant_pro_player_dict_creator(single_player_html, headings_list_html)
        player_list.append(player_stats)
    return player_list

def fant_pro_player_dict_creator(single_player_html, headings_list_html):
    """Take in html table row for a single player and return stats in list form"""
    single_player = {}
    counter = 0
    while counter < len(single_player_html):
        if counter == 1:
            name_team_pos = single_player_html[1].xpath("descendant::*/text()")
            if name_team_pos[0] is None or name_team_pos[0] == " ()":
                counter = len(single_player_html)
                continue
            single_player["NAME"] = name_team_pos[0]
            single_player["TEAM"] = name_team_pos[2]
            name_team_pos[3] = name_team_pos[3].strip(" - ")
            name_team_pos[3] = name_team_pos[3].strip(")")
            single_player["POS"] = name_team_pos[3]
        else:
            stat = single_player_html[counter].xpath("self::*/text()")
            if len(stat) != 0:
                single_player[headings_list_html[counter]] = stat[0]
        counter += 1
    return single_player

def yahoo_fa(league_no, b_or_p):
    """Parse FAs from yahoo league"""
    count = 0
    avail_player_list = []
    while count <= 300:
        # url = ("http://baseball.fantasysports.yahoo.com/b1/" + str(league_no) +
        #        "/players?status=A&pos=" + b_or_p + "&cut_type=33&stat1=S_S_2017&myteam=0&sort=AR&sdir=1&count=" +
        #        str(count))
        url = ("http://baseball.fantasysports.yahoo.com/b1/{league_no}" +
               "/players?status=A&pos={b_or_p}&cut_type=33&stat1=S_S_2017&myteam=0&sort=AR&" +
               "sdir=1&count={count}").format(league_no=league_no, b_or_p=b_or_p, count=count)
        content = urllib2.urlopen(url).read().decode('utf-8')
        content = unicodedata.normalize('NFKD', content).encode('ASCII', 'ignore')
        document = html.document_fromstring(content)
        body_html = document.xpath(".//div[@class='players'][table]/table/tbody/tr")
        for player_html in body_html:
            single_player_html = player_html.xpath("descendant::td")
            player_stats = yahoo_player_dict_creator(single_player_html)
            avail_player_list.append(player_stats)
        count += 25
    return avail_player_list

def yahoo_player_dict_creator(single_player_html):
    """Take in html table row for a single player and return stats in list form"""
    single_player = {}
    counter = 1
    dict_key_list = ["STARRED", "NAME", "TEAM", "POS", "OWNER", "GP", "PRESEASON_RANK",
                     "CURRENT_RANK", "PCT_OWN", "HAB", "R", "HR", "RBI", "SB", "OPS"]
    while counter < len(single_player_html):
        if counter == 1:
            name = single_player_html[1].xpath("descendant::a[@class='Nowrap name F-link']" +
                                               "/text()")[0]
            if name is None:
                counter = len(single_player_html)
                continue
            single_player[dict_key_list[1]] = name
            team_pos = single_player_html[1].xpath("descendant::span[@class='Fz-xxs']" +
                                                   "/text()")[0]
            single_player[dict_key_list[2]] = team_pos.split(" - ")[0]
            single_player[dict_key_list[3]] = team_pos.split(" - ")[1]
            counter = 6
            continue
        else:
            stat = single_player_html[counter].xpath("descendant::*/text()")
            if len(stat) != 0:
                single_player[dict_key_list[counter]] = stat[0]
        counter += 1
    return single_player

def yahoo_teams(league_no):
    """Parse teams from yahoo league"""
    team_list = []
    url = ("http://baseball.fantasysports.yahoo.com/b1/" + str(league_no) +
           "/startingrosters")
    content = urllib2.urlopen(url).read().decode('utf-8')
    content = unicodedata.normalize('NFKD', content).encode('ASCII', 'ignore')
    document = html.document_fromstring(content)
    team_divs = document.xpath(".//div[@class='Bd']/div")
    for team in team_divs:
        team_dict = yahoo_team_creator(team)
        team_list.append(team_dict)
    return team_list

def yahoo_team_creator(single_team_html):
    """Create team. Includes name, number, and roster (list)"""
    team = {}
    dict_key_list = ["TEAM_NAME", "TEAM_NUMBER", "ROSTER"]
    team[dict_key_list[0]] = str(single_team_html.xpath(".//p/a[@href]/text()")[0])
    team_number_a = single_team_html.xpath(".//p/a")[0]
    team[dict_key_list[1]] = team_number_a.attrib['href'].split("/")[3]
    table_body = single_team_html.xpath(".//table/tbody")
    for row in table_body:
        team[dict_key_list[2]] = row.xpath(".//tr/td[@class='player']/div[1]/div/a/text()")
    return team

def get_single_yahoo_team(league_no, team_name=None, team_number=None):
    """Get single team from yahoo team list. Using either team name or team number."""
    team_list = yahoo_teams(league_no)
    for team in team_list:
        if team_number is not None and team['TEAM_NUMBER'] == str(team_number):
            return team
        elif team_name is not None and team['TEAM_NAME'] == team_name:
            return team
    print "Team Name or Team Number are invalid."

# print fantasy_pro_players(ROS_PITCHER_URL)
