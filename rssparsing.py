import urllib2, sys
from xml.dom import minidom

sys.path.insert(0, 'libs/feedparser')
import feedparser


def get_fakebb_rss_content(entry):
    url = "http://feeds.feedburner.com/TheFakeBaseball?format=xml"

    content = feedparser.parse(url)

    if content.bozo:
        category = ""
        title = ""
        pubDate = ""
        dcCreator = ""
        pic = ""
        link = ""
        comments = ""
    else:
        category = content.entries[entry].category
        title = content.entries[entry].title
        # pubDate = content['entries'][entry]['pubDate']
        # dcCreator = content['entries'][entry]['dc:creator']
        pubDate = ""
        dcCreator = ""
        pic = content.entries[entry].description
        link = content.entries[entry].link
        comments = content.entries[entry].comments

    article = {"category":category, "title":title, "pubDate":pubDate, "dcCreator":dcCreator, "pic":pic, "link":link, "comments":comments}

    return article

def get_yahoo_rss_content(entry):
    url = "http://sports.yahoo.com/mlb/rss.xml"

    content = feedparser.parse(url)

    if content.bozo:
        category = ""
        title = ""
        pubDate = ""
        mediaCredit = ""
        mediaContent = ""
        pic = ""
        link = ""
        guid = ""
    else:
        category = content.entries[entry].category
        title = content.entries[entry].title
        # pubDate = content['entries'][entry]['pubDate']
        # mediaCredit = content['entries'][entry]['media:credit']
        # mediaContent = content['entries'][entry]['media:content']
        pubDate = ""
        mediaCredit = ""
        mediaContent = ""
        pic = content.entries[entry].description
        link = content.entries[entry].link
        guid = content.entries[entry].guid

    article = {"category":category, "title":title, "pubDate":pubDate, "mediaCredit":mediaCredit, "pic":pic, "mediaContent":mediaContent, "link":link, "guid":guid}

    return article
