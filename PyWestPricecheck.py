# ---------------------------------------------------------------------------   
# PyWestPricecheck.py - To check southwest flights (currently only one way)             

# Created by Justin Perket                                          
# 2017-05-16                                                                    


# Usage: python PyWestPricecheck.py [-t|--to] dest_port [-f|--from] origin_port [-d|--outdate] "outbound date (MM/DD/YYYY)

# requires: selenium, chromedriver (may be finicky on different systems)
# Revision history:                                                             
#                                                                               
# ---------------------------------------------------------------------------   




from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from optparse import OptionParser
from datetime import datetime
from datetime import timedelta
from time import sleep
import os

parser = OptionParser()
parser.add_option("-t", "--to", action="store", dest="dest_port",
                  help="destination airport (3 letter code)", type="string")
parser.add_option("-f", "--from", action="store", dest="origin_port",
                  help="origin airport (3 letter code)", type="string")
parser.add_option("-d", "--outdate", action="store", dest="out_date",
                  help="outbound date (MM/DD/YYYY)", type="string")
# # for future 2-way trip:
#parser.add_option("-rd", "--returndate", action="store", dest="return_date",
#                  help="return date (MM/DD/YYYY)", type="string")
#parser.add_option("-w", "--wau", action="store", dest="trip_way",
#                  help="1-way: -w 1, 2-way: -w 2", type="int")

(options, args) = parser.parse_args()

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()
# create a wait driver
wait = WebDriverWait(driver,10)
# Get webiste
driver.get("https://www.southwest.com/flight/")
print driver.title

# # get text boxes for airports
depart_from =  driver.find_element_by_id("originAirport_displayed")
fly_to = driver.find_element_by_id("destinationAirport_displayed")
# # NOTE: ONLY DO ONE WAY FOR NOW:
oneway=driver.find_element_by_id("oneWay").click()
# # get boxes for dates
outbound_date=driver.find_element_by_id("outboundDate")
#return_date=driver.find_element_by_id("outboundDate")

# # insert data
sleep(2)
depart_from.send_keys(Keys.CLEAR);
depart_from.send_keys(options.dest_port)
depart_from.send_keys(Keys.TAB);
fly_to.send_keys(Keys.CLEAR);
fly_to.send_keys(options.origin_port)
fly_to.send_keys(Keys.TAB);
outbound_date.send_keys(Keys.CONTROL + "a");
outbound_date.send_keys(Keys.DELETE);
outbound_date.send_keys(options.out_date)
outbound_date.send_keys(Keys.TAB);

#click the search button
driver.find_element_by_id("submitButton").click()
