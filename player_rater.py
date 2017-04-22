"""Rate players"""

def rate_fa(fa_list, ros_projection_list):
    """Compare available FAs with Projections"""
    fa_player_list = []
    for player in ros_projection_list:
        if any(fa['NAME'].lower().replace('.', '') ==
               player.name.lower().replace('.', '') for fa in fa_list):
            player.isFA = True
            fa_player_list.append(player)
    dollar_value = 100.00
    player_number = 0
    if "P" in ros_projection_list[0].pos:
        while dollar_value > 1.0:
            print ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^20}" +
                   " - {player.wins:^3} - {player.svs:^2} - {player.sos:^3} - {player.era:^4}" +
                   " - {player.whip:^4}").format(player=fa_player_list[player_number])
            dollar_value = fa_player_list[player_number].dollarValue
            player_number += 1
    else:
        while dollar_value > 1.0:
            print ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^20}" +
                   " - {player.runs:^3} - {player.hrs:^2} - {player.rbis:^3} - {player.sbs:^2}" +
                   " - {player.ops:^5}").format(player=fa_player_list[player_number])
            dollar_value = fa_player_list[player_number].dollarValue
            player_number += 1

def rate_team(team_dict, ros_projection_list):
    """Compare team with Projections"""
    team_roster_list = [roster.lower().replace('.', '') for roster in team_dict['ROSTER']]
    team_player_list = []
    for player in ros_projection_list:
        if player.name.lower().replace('.', '') in team_roster_list:
            team_player_list.append(player)
    for player in team_player_list:
        if "P" in ros_projection_list[0].pos:
            print ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^20}" +
                   " - {player.wins:^3} - {player.svs:^2} - {player.sos:^3} - {player.era:^4}" +
                   " - {player.whip:^4}").format(player=player)
        else:
            print ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^20}" +
                   " - {player.runs:^3} - {player.hrs:^2} - {player.rbis:^3} - {player.sbs:^2}" +
                   " - {player.ops:^5}").format(player=player)
