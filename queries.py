"""GQL Queries"""
import logging
import player_models
import db_models
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
    batter_query = player_models.BatterDB.all()
    batter_query.filter("normalized_first_name =", player_name['First'])
    batter_query.filter("last_name =", player_name['Last'])
    batter_table = batter_query.run()
    batter = list(batter_table)
    return batter

def get_single_pitcher(player_name):
    # logging.info("\r\n*******************\r\nget_single_pitcher QUERY")
    pitcher_query = player_models.PitcherDB.all()
    pitcher_query.filter("normalized_first_name =", player_name['First'])
    pitcher_query.filter("last_name =", player_name['Last'])
    pitcher_table = pitcher_query.run()
    pitcher = list(pitcher_table)
    return pitcher

# User Queries
def get_user(username):
    user_query = db_models.User.all()
    user_query.filter("username =", username)
    user_list = list(user_query)
    return user_list[0]

def check_username(username):
    # n = db.GqlQuery("SELECT * FROM Users ORDER BY username") #pull db of userinfo and order by username
    name = db_models.User.all().order("username") # .all() = "SELECT *"; .order("username") = "ORDER BY username"
    for n in name:
        if n.username == username:
            return n.key().id()

def get_user_by_name(username):
    """ Get a user object from the db, based on their username """
    # user = db.GqlQuery("SELECT * FROM Users WHERE username = '%s'" % username) #using %s in SQL queries is BAD, never do this
    user = db_models.User.all().filter("username", username) # .all() = "SELECT *"; .filter("username", username) = "username = username"
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
