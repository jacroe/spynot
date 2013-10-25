SpyNot Server
======

This server is used for the [Three Amigos Software Development's](https://www.facebook.com/groups/595385207185991/) SpyNot application. The API can be queried with a search term, a package name, or with a category and subcategory. It uses @egirault's [googleplay-api](https://github.com/egirault/googleplay-api) package to talk with Google's servers.

1. *SearchApp*: Upon receipt of a search term, the server will query the Google Play's servers for apps that match those terms. The server will return a list of 20 apps that contain the app's title, author' whether they're a super developer or not, the Play rating, an icon, and the package name.
2. *GetDetails*: This method returns more detailed information about a package name. It returns the title, author, app description, cost, an icon, category, a list of permissions, the number of downloads, the Play rating, and the Google Play url.
3. *GetAppPermissionsByCategory*: This returns an array of package names and their relevant permissions.