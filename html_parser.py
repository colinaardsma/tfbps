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
        player_stats = single_player_stat_list_creator(single_player_html, headings_list_html)
        player_list.append(player_stats)
    return player_list

def single_player_stat_list_creator(single_player_html, headings_list_html):
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

# print fantasy_pro_batters(ROS_BATTER_URL)
