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
    logging.info("*******************\r\nget_single_batter QUERY")
    batter = player_models.BatterDB.all()
    batter.filter("normalized_first_name =", player_name['First'])
    batter.filter("last_name =", player_name['Last'])
    return batter

def get_single_pitcher(player_name):
    logging.info("*******************\r\nget_single_pitcher QUERY")
    pitcher = player_models.PitcherDB.all()
    pitcher.filter("normalized_first_name =", player_name['First'])
    pitcher.filter("last_name =", player_name['Last'])
    return pitcher
