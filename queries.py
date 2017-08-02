"""GQL Queries"""
import logging
import player_models
# from google.appengine.ext import db

# Projection Queries
def get_batters():
    # logging.info("*******************\r\nget_batters QUERY")
    batter_table = player_models.BatterDB.all().order("-fvaaz") # .all() = "SELECT *"; .order("-sgp") = "ORDER BY sgp DESC"
    # players = query.fetch()
    batters = list(batter_table)
    return batters

def get_pitchers():
    # logging.info("*******************\r\nget_pitchers QUERY")
    pitcher_table = player_models.PitcherDB.all().order("-fvaaz") # .all() = "SELECT *"; .order("-sgp") = "ORDER BY sgp DESC"
    # players = query.fetch()
    pitchers = list(pitcher_table)
    return pitchers

def get_single_batter(player_name):
    # logging.info("\r\n*******************\r\nget_single_batter QUERY")
    batter_table = player_models.BatterDB.all()
    batter_table.filter("normalized_first_name =", player_name['First'])
    batter_table.filter("last_name =", player_name['Last'])
    batter = list(batter_table)
    return batter

def get_single_pitcher(player_name):
    # logging.info("\r\n*******************\r\nget_single_pitcher QUERY")
    pitcher_table = player_models.PitcherDB.all()
    pitcher_table.filter("normalized_first_name =", player_name['First'])
    pitcher_table.filter("last_name =", player_name['Last'])
    pitcher = list(pitcher_table)
    return pitcher
