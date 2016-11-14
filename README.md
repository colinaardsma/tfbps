# tFBPs (the Fantasy Baseball Projection site)
A fantasy baseball projection site.

## What it does
While still very much a work in progress I have acheived a few of my main goals:
* Data import/export/analysis:
    * Parse HTML projection (table) data from external sites.
    * Store data in SQL database.
    * Analyze data and return value for each player.
    * Store data in memcache to prevent excessive db hits.
    * Export data to json
* Users:
    * Login/Logout/Register
    * Divide users into groups with permissions varying by group
* Blog/Posts:
    * Allow certain users to post to blog
    * Create/Read/Update/Delete blog posts
* RSS import:
    * Import and format RSS data from external sites
## What to do
1. First, register a user or two for testing via the register link on the login page. (Notice how we've already implemented that one for you!)
2. You have a few TODOs left in the comments (open **Window > Show View > Tasks** and sort by Path for a handy guide). The first is to implement quote lookup. You'll find the request handler for this action in `StockController.java`, and templates in `quote_form.html` and  `quote_display.html`. Take it from there, using the parameters already put in place for you in the template.
3. We failed to make the `symbol` field of `StockHolding.java` case-insensitive, which will cause unintended results when buying and selling. Fix this by updating the appropriate constructor for the `StockHolding` class to make the symbol either always be upper or lowercase (your choice). You'll also have to update the static `buyShares` and `sellShares` methods in the same class.
4. Implement buy and sell. You'll find request handlers in `StockController.java`, relevant model methods in `StockHolding.java`, and a shared buy/sell template in `transaction_form.html` and `transaction_confirm.html`. Note that you're making changes that should be persisting data in the database, so be sure that's happening correctly before checking this one off your list. You'll have to deal with a `StockLookupException` in some cases. Your controller should `try/catch` the affected calls and respond appropriately (hint: see `AbstractFinanceController.displayError` and it's usage in other locations within the project).
5. Now that you can buy and sell, let's make sure our users can't buy indefinitely (we forgot to give them a cash limit). Add a `cash` field to the `User` model class, making sure to include the proper persistence annotations. Then, update the user's cash on buy/sell requests, and handle a request to buy that exceeds available funds appropriately.
6. Display the user's stocks in a table. You'll find some code already in place in `PortfolioController.java` and the `portfolio.html` template. You should display the following fields for each stock in the template: display name (use `Stock.toString()`), number of shares owned, current price, and total value of shares owned. Format the currency values appropriately, with 2 decimal places. You may find the `th:each` Thymleaf tag useful here.

[stocks-repo]: https://github.com/LaunchCodeEducation/spring-stocks
