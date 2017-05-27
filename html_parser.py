"""HTML Parsing"""
import urllib2
import unicodedata
from lxml import html

def html_to_document(url):
    """Get league standings\n
    Args:\n
        url: the url.\n
    Returns:\n
        html in document form.\n
    Raises:\n
        None.
    """
    content = urllib2.urlopen(url).read().decode('utf-8')
    content = unicodedata.normalize('NFKD', content).encode('ASCII', 'ignore')
    document = html.document_fromstring(content)
    return document

def fantasy_pro_players(url):
    """Parse batter data from url\n
    Args:\n
        url: the fantasypros.com url.\n
    Returns:\n
        list of dict of player projections.\n
    Raises:\n
        None.
    """
    document = html_to_document(url)
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
    """Take in html table row for a single player and return player data and
    stats in dictionary form.\n
    Args:\n
        single_player_html: html for a single player.\n
        headings_list_html: html for the table heading row.\n
    Returns:\n
        dict of projections for a single player.\n
    Raises:\n
        None.
    """
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
    """Parse FAs from yahoo league\n
    Args:\n
        league_no: Yahoo! fantasy baseball league number.\n
        b_or_p: "B" for batters or "P" for pitchers.\n
    Returns:\n
        list of available FAs for league specified.\n
    Raises:\n
        None.
    """
    count = 0
    avail_player_list = []
    while count <= 300:
        url = ("http://baseball.fantasysports.yahoo.com/b1/{league_no}" +
               "/players?status=A&pos={b_or_p}&cut_type=33&stat1=S_S_2017&myteam=0&sort=AR&" +
               "sdir=1&count={count}").format(league_no=league_no, b_or_p=b_or_p.upper(),
                                              count=count)
        document = html_to_document(url)
        body_html = document.xpath(".//div[@class='players'][table]/table/tbody/tr")
        for player_html in body_html:
            single_player_html = player_html.xpath("descendant::td")
            player_stats = yahoo_player_dict_creator(single_player_html, b_or_p.upper())
            avail_player_list.append(player_stats)
        count += 25
    return avail_player_list

def yahoo_player_dict_creator(single_player_html, b_or_p):
    """Take in html table row for a single player and return stats in list form\n
    Args:\n
        single_player_html: html for a single player.\n
        b_or_p: "B" for batters or "P" for pitchers.\n
    Returns:\n
        dict of projections for a single player.\n
    Raises:\n
        None.
    """
    single_player = {}
    counter = 1
    if b_or_p == "B":
        dict_key_list = ["STARRED", "NAME", "TEAM", "POS", "OWNER", "GP", "PRESEASON_RANK",
                         "CURRENT_RANK", "PCT_OWN", "HAB", "R", "HR", "RBI", "SB", "OPS"]
    else:
        dict_key_list = ["STARRED", "NAME", "TEAM", "POS", "OWNER", "GP", "PRESEASON_RANK",
                         "CURRENT_RANK", "PCT_OWN", "IP", "W", "SV", "K", "ERA", "WHIP"]
    while counter < len(single_player_html) and counter < 15:
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
    """Parse teams from yahoo league\n
    Args:\n
        league_no: Yahoo! fantasy baseball league number.\n
    Returns:\n
        list of teams based on league number.\n
    Raises:\n
        None.
    """
    team_list = []
    url = ("http://baseball.fantasysports.yahoo.com/b1/" + str(league_no) +
           "/startingrosters")
    document = html_to_document(url)
    team_divs = document.xpath(".//div[@class='Bd']/div")
    for team in team_divs:
        team_dict = yahoo_team_creator(team)
        team_list.append(team_dict)
    return team_list

def yahoo_team_creator(single_team_html):
    """Create team. Includes name, number, and roster (list)\n
    Args:\n
        single_team_html: html for a single team.\n
    Returns:\n
        dict of team including name, number, and roster as a list.\n
    Raises:\n
        None.
    """
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
    """Get single team from yahoo team list. Using either team name or team number.\n
    Args:\n
        league_no: Yahoo! fantasy baseball league number.\n
        team_name: name of the team to retreive (default = None).
        team_number: number of the team to retreive (default = None).
    Returns:\n
        dict of single team.\n
    Raises:\n
        None.
    """
    team_list = yahoo_teams(league_no)
    for team in team_list:
        if team_number is not None and team['TEAM_NUMBER'] == str(team_number):
            return team
        elif team_name is not None and team['TEAM_NAME'] == team_name:
            return team
    print "Team Name or Team Number are invalid."

def get_standings(league_no, team_count):
    """Get league standings\n
    Args:\n
        league_no: Yahoo! fantasy baseball league number.\n
        team_count: number of teams in league.\n
    Returns:\n
        list of dict of current team standings.\n
    Raises:\n
        None.
    """
    url = ("http://baseball.fantasysports.yahoo.com/b1/" + str(league_no) +
           "/standings?opt_out=1")
    document = html_to_document(url)
    points_html = document.xpath(".//section[@id='standings-table']/table")[0]
    points_headers = points_html.xpath(".//thead/tr[@class='Alt Last']//text()")
    points_header_list = []
    for header_html in points_headers:
        if header_html == u"\ue004":
            continue
        header = "Points" + header_html.replace(" ", "")
        points_header_list.append(header)
    points_teams = points_html.xpath(".//tbody/tr")
    stats_html = document.xpath(".//section[@id='standings-table']/table")[1]
    stats_headers = stats_html.xpath(".//thead/tr[@class='Alt Last']//text()")
    stats_header_list = []
    for header_html in stats_headers:
        if header_html == u"\ue004":
            continue
        header = "Stats" + header_html.replace(" ", "")
        stats_header_list.append(header)
    stats_teams = stats_html.xpath(".//tbody/tr")
    current_standings = []
    html_counter = 0
    while html_counter < team_count:
        team_dict = {}
        team_points_row = points_teams[html_counter].xpath(".//descendant::text()")
        team_stats_row = stats_teams[html_counter].xpath(".//descendant::text()")
        team_points_row[0] = team_points_row[0].replace(".", "")
        team_stats_row[0] = team_stats_row[0].replace(".", "")
        points_counter = 0
        while points_counter < len(points_header_list):
            team_dict[points_header_list[points_counter]] = team_points_row[points_counter]
            points_counter += 1
        stats_counter = 0
        while stats_counter < len(stats_header_list):
            team_dict[stats_header_list[stats_counter]] = team_stats_row[stats_counter]
            stats_counter += 1
        current_standings.append(team_dict)
        html_counter += 1
    return current_standings

# def single_team_standing_dict(league_no, current_standings, team_name=None, team_number=None):
#     """Get league standings\n
#     Args:\n
#         league_no: Yahoo! fantasy baseball league number.\n
#         current_standings: dict of the current league standings.\n
#     Returns:\n
#         list of dict of projected final team standings.\n
#     Raises:\n
#         None.
#     """
#     projected_final_standings = []
#     team_list = yahoo_teams(league_no)
#     return projected_final_standings

def get_league_settings(league_no):
    """Get league settings\n
    Args:\n
        league_no: Yahoo! fantasy baseball league number.\n
    Returns:\n
        dict of league settings.\n
    Raises:\n
        None.
    """
    url = ("http://baseball.fantasysports.yahoo.com/b1/" + str(league_no) +
           "/settings")
    document = html_to_document(url)
    settings_table = document.xpath(".//table[@id='settings-table']/tbody")[0]
    league_settings = {}
    settings_rows = settings_table.xpath(".//tr")
    for setting in settings_rows:
        key = setting.xpath(".//td/text()")[0].encode('utf-8').strip().replace('\xc2\xa0', ' ')
        if key == "League Logo:":
            continue
        value = setting.xpath(".//td/b/text()")[0].encode('utf-8').strip().replace('\xc2\xa0', ' ')
        league_settings[key] = value
    return league_settings

def split_league_pos_types(league_roster_pos):
    """Turn full list of league roster spots into list split into batting, pitching, bench, dl, na\n
    Args:\n
        league_roster_pos: list of roster spots\n
    Returns:\n
        dict of roster spots by type (batting, pitching, bench, dl, na.\n
    Raises:\n
        None.
    """
    batting_pos = []
    pitching_pos = []
    bench_pos = []
    dl_pos = []
    na_pos = []
    all_pos = league_roster_pos.split(", ")
    while "SP" in all_pos:
        pitching_pos.append("SP")
        all_pos.remove("SP")
    while "RP" in all_pos:
        pitching_pos.append("RP")
        all_pos.remove("RP")
    while "P" in all_pos:
        pitching_pos.append("P")
        all_pos.remove("P")
    while "BN" in all_pos:
        bench_pos.append("BN")
        all_pos.remove("BN")
    while "DL" in all_pos:
        dl_pos.append("DL")
        all_pos.remove("DL")
    while "NA" in all_pos:
        na_pos.append("NA")
        all_pos.remove("NA")
        batting_pos = all_pos
    league_roster_pos_dict = {}
    league_roster_pos_dict["Batting POS"] = batting_pos
    league_roster_pos_dict["Pitching POS"] = pitching_pos
    league_roster_pos_dict["Bench POS"] = bench_pos
    league_roster_pos_dict["DL POS"] = dl_pos
    league_roster_pos_dict["NA POS"] = na_pos
    return league_roster_pos_dict

# print split_leauge_pos_types(get_league_settings(5091)["Roster Positions:"])


LEAGUE_NO = 5091
TEAM_COUNT = 12
CURRENT_STANDINGS = get_standings(LEAGUE_NO, TEAM_COUNT)

# print single_team_standing_dict(LEAGUE_NO, CURRENT_STANDINGS)
