#!/usr/bin/env python
# ---------------------------------------------------------------------------   
# PyWestPricecheck.py - To check southwest flights (currently only one way)             

# Created by Justin Perket  (JustinPerket@gmail.com)
# 2017-05-16                                                                    


# Usage: PyWestPricecheck.py [-t|--to] dest_port [-f|--from] origin_port 
#    [-d|--outdate] "outbound date (MM/DD/YYYY)

# Requires: selenium, chromedriver (may be finicky on different systems)
#
# Todo: add non-nonstop option, screen by flight number option. Perhaps screen for time range?
# ---------------------------------------------------------------------------   

import argparse
from bs4 import BeautifulSoup
import re
import time 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from pyvirtualdisplay import Display

def flightinputs():
    parser = argparse.ArgumentParser(description="Periodically runs and monitors PyWestcheck in console")
    parser.add_argument("-t", "--to", dest="dest_port",
                      help="destination airport (3 letter code)", required=True)
    parser.add_argument("-f", "--from", dest="origin_port",
                      help="origin airport (3 letter code)", required=True)
    parser.add_argument("-d", "--outdate", dest="out_date",
                      help="outbound date (MM/DD/YYYY)", required=True)
    # # Uncomment this in future for 2-way trip:
    # parser.add_argument("-rd", "--returndate", action="store", dest="return_date",
    #                  help="return date (MM/DD/YYYY)", type="string")
    # parser.add_argument("-w", "--wau", action="store", dest="trip_way",
    #                  help="1-way: -w 1, 2-way: -w 2", type="int")
    #  

    #options = parser.parse_args()
    options = parser.parse_args('-t MKE -f DEN -d 07/26/17'.split()) # For testing, make up data
    return options
    
def pricecheck(options):
    
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()
    # create a wait driver
    WebDriverWait(driver, 20)
    # Get website:
    driver.get("https://www.southwest.com/flight/")
    print("Checking on: " + time.strftime('%X %x'))

    # Get text boxes for airports
    depart_from = driver.find_element_by_id("originAirport_displayed")
    fly_to = driver.find_element_by_id("destinationAirport_displayed")
    # NOTE: ONLY DO ONE WAY FOR NOW:
    driver.find_element_by_id("oneWay").click()
    # get boxes for dates
    outbound_date = driver.find_element_by_id("outboundDate")
    # return_date=driver.find_element_by_id("outboundDate")

    # # Insert flight input:
    WebDriverWait(fly_to, 20)    
    fly_to.click(); fly_to.click();  # make sure page and box is selected
    fly_to.send_keys(Keys.CLEAR);
    fly_to.send_keys(options.origin_port)
    fly_to.send_keys(Keys.TAB);

    depart_from.click();  
    depart_from.send_keys(Keys.CLEAR);
    depart_from.send_keys(options.dest_port)
    depart_from.send_keys(Keys.TAB);

    outbound_date.click()
    outbound_date.send_keys(Keys.CONTROL + "a");
    outbound_date.send_keys(Keys.DELETE);
    outbound_date.send_keys(options.out_date)
    outbound_date.send_keys(Keys.TAB);

    # Click the search button and wait for new page
    driver.find_element_by_id("submitButton").click()

    # Now scrape page (may be a simpler way to do this,
    # but I want to learn how to use BeautifulSoup
    WebDriverWait(driver.page_source, 20); time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Handily, southwest currently has all  flight info in the selection radios,
    # with names in the formate "Out[row#][A-C]", where A=Business,B=Anytime,C=Wanna Get Away Prices.
    # Let's search for the cheapest (C). This finds all id's named like "Out[0-99]C"
    flight_results = soup.find_all(id=re.compile("^Out[1-9]?[0-9]C$"))

    # Start printing to output           
    labels = ['Flight No.', 'Price', 'Departure', 'Arrival', 'Stops'.rjust(15)]
    grid_list = [[]]  # create a nested list to return
    grid_list[0] = ''.join('{: >15}'.format(stri).ljust(10) for stri in labels)  # const. width formatting
    # print grid_list[0] # print labels row
        
    for flight in flight_results:
        # The delicious data is in the title attribute:
        flightstr = str(flight.attrs['title'])
        if flightstr.find("Nonstop") != -1:  # Screen for direct flights
            # get and format data we want:
            filist = flightstr.split(' ', 8)
            filist2 = [filist[2], filist[3], filist[4], filist[6], filist[8]]
            grid_list.append(''.join('{: >15}'.format(stri).rjust(2) for stri in filist2))       
    
    for row in grid_list:
        print(row)
    
    # Now close up:            
    driver.close()
    return(grid_list)


def main():
    # run headless, in invisible virtual display:
    # display = Display(visible=0, size=(1600, 900))
    # display.start()
    
    options = flightinputs()
    pricecheck(options)
    
    # display.stop()

            
        
if __name__ == "__main__":
    main()
