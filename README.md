# tFBPs (the Fantasy Baseball Projection site)
A fantasy baseball projection site.

## What it does
While still very much a work in progress I have acheived a few of my main goals:
* Data import/export/analysis:
    * Parse HTML projection (table) data from external sites
    * Store data in SQL database
    * Analyze data and return value for each player
    * Store data in memcache to prevent excessive db hits
    * Export data to json
* Users:
    * Login/Logout/Register
    * Divide users into groups with permissions varying by group
* Blog/Posts:
    * Allow certain users to post to blog
    * Create/Read/Update/Delete blog posts
* RSS import:
    * Import and format RSS data from external sites

## What's coming up
* Data import/export/analysis:
    * Allow users to create their own calculations
    * Connect with Yahoo! fantasy sports API to allow users to import custom league data
    * Allow custom calculations based on Yahoo! imported data
* Users:
    * Storing of personalized data
* Blog/Posts:
    * Add snippets to main page
