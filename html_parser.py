"""HTML Parsing"""
import urllib2
from lxml import html

ROS_BATTER_URL = "http://www.fantasypros.com/mlb/projections/ros-hitters.php"

def fantasy_pro_batters(url):
    """Parse batter data from url"""
    content = urllib2.urlopen(url).read()
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

def yahoo_batter_fa(league_no):
    """Parse Batter FAs from yahoo league"""
    count = 0
    avail_player_list = []
    while count <= 300:
        url = ("http://baseball.fantasysports.yahoo.com/b1/" + str(league_no) +
               "/players?status=A&pos=B&cut_type=33&stat1=S_S_2017&myteam=0&sort=AR&sdir=1&count=" +
               str(count))
        content = urllib2.urlopen(url).read()
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


        # tostring = html.tostring(body_html[0], pretty_print=True, method="html")



# print yahoo_batter_fa(5091)
