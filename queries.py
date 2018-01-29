"""GQL Queries"""
import logging
import player_models
import db_models
# from google.appengine.ext import db

# Projection Queries
def get_batters():
    # logging.info("*******************\r\nget_batters QUERY")
    batter_table = player_models.BatterProj.query().order(-player_models.BatterProj.fvaaz) # .query() = "SELECT *"; .order("-sgp") = "ORDER BY sgp DESC"
    # players = query.fetch()
    batters = list(batter_table)
    return batters

def get_pitchers():
    # logging.info("*******************\r\nget_pitchers QUERY")
    pitcher_table = player_models.PitcherProj.query().order(-player_models.BatterProj.fvaaz) # .query() = "SELECT *"; .order("-sgp") = "ORDER BY sgp DESC"
    # players = query.fetch()
    pitchers = list(pitcher_table)
    return pitchers

def get_single_batter(player_name):
    # logging.info("\r\n*******************\r\nget_single_batter QUERY")
    batter_query = player_models.BatterProj.query()
    batter_query.filter(player_models.BatterProj.normalized_first_name == player_name['First'])
    batter_query.filter(player_models.BatterProj.last_name == player_name['Last'])
    batter_table = batter_query.run()
    batter = list(batter_table)
    return batter

def get_single_pitcher(player_name):
    # logging.info("\r\n*******************\r\nget_single_pitcher QUERY")
    pitcher_query = player_models.PitcherProj.query()
    pitcher_query.filter(player_models.PitcherProj.normalized_first_name == player_name['First'])
    pitcher_query.filter(player_models.PitcherProj.last_name == player_name['Last'])
    pitcher_table = pitcher_query.run()
    pitcher = list(pitcher_table)
    return pitcher

# User Queries
def get_user(username):
    user_query = db_models.User.query()
    user_query.filter(db_models.User.username == username)
    user_list = list(user_query)
    return user_list[0]

def check_username(username):
    # n = db.GqlQuery("SELECT * FROM Users ORDER BY username") #pull db of userinfo and order by username
    name = db_models.User.query().order(db_models.User.username) # .query() = "SELECT *"; .order("username") = "ORDER BY username"
    for n in name:
        if n.username == username:
            return n.key().id()

def get_user_by_name(username):
    """ Get a user object from the db, based on their username """
    # user = db.GqlQuery("SELECT * FROM Users WHERE username = '%s'" % username) #using %s in SQL queries is BAD, never do this
    user = db_models.User.query().filter(db_models.User.username == username) # .query() = "SELECT *"; .filter("username", username) = "username = username"
    if user:
        return user.get()

def get_user_by_id(user_id):
    # logging.error("get_user_by_uid QUERY")
    """ Get a user object from the db, based on their username """
    user = db_models.User.get_by_id(int(user_id))
    if user:
        return user

def get_authorization(username):
    user = get_user_by_name(username)
    if user:
        return user.authorization

# League Queries
def get_all_user_leagues_by_user(user):
    # logging.info("*******************\r\nget_batters QUERY")
    user_leagues_table = db_models.User_League.query().filter(db_models.User_League.user == user)
    user_leagues = list(user_leagues_table)
    return user_leagues

def get_leagues_by_user(user):
    # logging.info("*******************\r\nget_batters QUERY")
    user_leagues = get_all_user_leagues_by_user(user)
    league_list = []
    for user_league in user_leagues:
        league = db_models.League.query().filter(db_models.League.Key == user_league.league)
        league_list.append(league)
    return league_list

def get_all_leagues():
    # logging.info("*******************\r\nget_batters QUERY")
    league_table = db_models.League.query()
    leagues = list(league_table)
    return leagues

def get_leagues_by_league_key(league_key):
    # logging.info("*******************\r\nget_batters QUERY")
    league = db_models.League.query().filter(db_models.League.league_key == league_key)
    if league:
        return league.get()
