This is a price tracker app that can track the prices for any website,
by default it will allow tracking for elitehubs only, 
to change the website you'll need to tinker a bit in the website url and which html component to find for the name and price

libraries needed to be installed: beautifulsoup4, requests

dataUpdate.py
this script is meant to be executed by a batchfile during startup,
it will track and update prices and date of the urls entered by users previously
this is basically the tracking script which automates the tracking for each day.

userMenu.py
this script is meant to be executed by user to input urls to be tracked
or to perform some function or display the prices of the items.

dataSet.csv
contains the item data of each url

urlData.csv
contains all the urls that've been inputted since inception.
