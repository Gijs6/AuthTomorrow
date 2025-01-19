# SomtodaySSOScraper

_SomtodaySSOScraper_ "automates" the process of logging into Somtoday by literally entering your username and password. The Somtoday auth is a huge mess, but this script could help get you the auth required for the [Somtoday API](https://github.com/elisaado/somtoday-api-docs). This is not a great system (ideally, you could just use an OAuth redirect, but they don't allow any other redirect URI's), but this works! (sometimes)

**Do not use this script for any sensitive or personal data unless you understand the potential risks.**

Please install `selenium` and `requests` (via pip) before running the script.

This script **does NOT work** if your school uses Microsoft, Google, or other external services to log into Somtoday.

If you can, please use [_Somtoday SSO tool_](https://github.com/m-caeliusrufus/Somtoday-SSO-tool/) or [_SomtodaySSOLogin_](https://github.com/Underlyingglitch/SomtodaySSOLogin), that is much safer. I just built this for the cases where you can't have an external login.
