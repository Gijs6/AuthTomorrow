# SomtodaySSOScraper

A Selenium-based script that "automates" the process of logging into Somtoday by entering your username and password. This allows you to fetch authentication tokens for accessing the [Somtoday API](https://github.com/elisaado/somtoday-api-docs). This is not a great system (ideally, there should be some code that just uses the login from Som, but they don't allow any other redirect URI's for the login), but it works (sometimes).

**Do not use this script for any sensitive or personal data unless you understand the potential risks.**

Please install `selenium` and `requests` (via pip) before running the script.

This script **does NOT work** if your school uses Microsoft, Google, or other external services to log into Somtoday.

Huge thanks to [m-caeliusrufus](https://github.com/m-caeliusrufus) for making [Somtoday SSO tool](https://github.com/m-caeliusrufus/Somtoday-SSO-tool/). The auth part is mostly based on that script.

