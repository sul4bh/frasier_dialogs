# About

This python package downloads the dialogs of the Fraiser sitcom. The dialogs are scraped from the website 
http://www.kacl780.net/frasier/transcripts/ and pertinent information are written to a sqlite database.

# Installation and running

1. Create a virtual environment `virtualenv venv`
1. Install requirements `pip install -r requirements.txt`
1. Install a webdriver binary `brew install chromedriver` or `http://selenium-python.readthedocs.io/installation.html#drivers`
1. Run the package `python3 -m frasier_dialogs --verbose`

The scraped data will be available in `fraiser.db` SQLite database.
