"""GQL Queries"""
import logging
import player_models
# from google.appengine.ext import db

# Projection Queries
def get_batters():
    logging.error("get_batters QUERY")
    batter_table = player_models.BatterDB.all().order("-fvaaz") # .all() = "SELECT *"; .order("-sgp") = "ORDER BY sgp DESC"
    # players = query.fetch()
    batters = list(batter_table)
    return batters

def get_pitchers():
    logging.error("get_pitchers QUERY")
    pitcher_table = player_models.PitcherDB.all().order("-fvaaz") # .all() = "SELECT *"; .order("-sgp") = "ORDER BY sgp DESC"
    # players = query.fetch()
    pitchers = list(pitcher_table)
    return pitchers
