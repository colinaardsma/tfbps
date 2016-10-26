from dbmodels import Users, FPProjB, FPProjP #import Users and Blog classes from python file named dbmodels
from google.appengine.ext import db
import logging
import gqlqueries

def set_authorization(user, auth):
    logging.error("set_authorization QUERY")
    """ Set user authorization in the db, based on their username """
    user = gqlqueries.get_user_by_name(user)
    user.authorization = auth
    user.put()
