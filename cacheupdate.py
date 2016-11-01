import math, time
import caching, main

def blog_cache_update(post="", usr="", update=False):
    #update cache
    time.sleep(.1) # wait 1/10 of a second while post is entered into db
    author = caching.cached_user_by_name(post.author.username) # pulls the user from the db by name passed through the url
    caching.cached_posts(None, 0, author, usr, True) # direct cached_posts to update cache
    caching.cached_posts(None, 0, "", "", True) # direct cached_posts to update cache

    limit = main.PostList.limit # number of entries displayed per page

    # update cache of pagination by user
    allPostsByauthor = caching.cached_posts(None, 0, author, usr)
    lastPageByauthor = math.ceil(len(allPostsByauthor) / float(limit)) # calculate the last page required based on the number of entries and entries displayed per page

    for i in range(int(lastPageByauthor), 0, -1):
        offset = (i - 1) * 5
        caching.cached_posts(limit, offset, author, usr, True) # direct cached_posts to update cache

    limit = main.PostList.limit # number of entries displayed per page

    # update cache of pagination for all posts
    allPosts = caching.cached_posts(None, 0, "", "")
    lastPage = math.ceil(len(allPosts) / float(limit)) # calculate the last page required based on the number of entries and entries displayed per page

    for i in range(int(lastPage), 0, -1):
        offset = (i - 1) * 5
        caching.cached_posts(limit, offset, "", "", True) # direct cached_posts to update cache
