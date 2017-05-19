#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ---------------------------------------------------------------------------   
# PyWestWatcher.py - Periodically runs and monitors PyWestcheck.          
#                    Sends an email alert when a new low price is found for 
#                    the flights being searched for
# Created by Justin Perket  (JustinPerket@gmail.com)
# 2017-05-16                                                                    


# Usage: PyWestWatcher.py [-t|--to] dest_port [-f|--from] origin_port 
#    [-d|--outdate] "outbound date (MM/DD/YYYY)

# Requires: selenium, chromedriver (may be finicky on different systems)
#
# Todo: use invisible display for browser
# ---------------------------------------------------------------------------   

from email.header    import Header
from email.mime.text import MIMEText
from getpass         import getpass
import PyWestPricecheck
import argparse
import os
import re
import smtplib
import socket
import time


# A place for argparse stuff    
def watchinputs(): 
    parser = argparse.ArgumentParser(
         description="Periodically runs and monitors PyWestcheck while running \
                     in console. Sends an email alert when a new low price is found\
                     for the flights being searched for",
         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--out_dir", dest="out_dir", default='./', help="destination of log file (default = current dir)", required=False)    
    parser.add_argument("--tint", dest="tint", default=0.01, help="time interval in hours (default=0.5hr)", required=False)    
    parser.add_argument("--maxdur", default=0.01, help="max duration to run in hours (default=10hr)", required=False)    
    
    options = parser.parse_args()
    return options


# Send an email alert. I made a throwaway yahoo email account for this
def sendalert_yahoogmail(yahoologin, password, bodytext, subjtext, toaddrs):
    fromaddr = yahoologin + "@yahoo.com"
    msg = MIMEText(bodytext, _charset='utf-8')
    msg['Subject'] = Header(subjtext, 'utf-8')
    msg['From'] = fromaddr
    msg['To'] = toaddrs 
     
    server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
    server.starttls()
    server.login(yahoologin, password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())    
    server.quit()      
    print("  Email sent!")

    
# Get info to search for flights ever [tint] hours, and logs retrievals.
# Checks if a new lower price has been retrieved. If so, emails an alert    
def main():    
    
    watchoptions = watchinputs()  # get watcher input args
    flightoptions = PyWestPricecheck.flightinputs()  # get flight info args

    # email details to send new low price alerts:
    toaddrs = "jperk2@gmail.com"  # email to send alerts to         
    yahoologin, password = "jp137.035999139", getpass("Yahoo password :")
        
    # Create and open log file, if doesn't exist:
    foutname = flightoptions.origin_port + "." + flightoptions.dest_port + "." + flightoptions.out_date.replace("/", "-")
    file_out = os.path.abspath(watchoptions.out_dir + "/PyWestLog." + foutname + ".txt")
    # fopen = open(file_out, "a")    
    
    # Init some stuff for the lpp[
    time0 = time.time()  # get current (Epoch) time 
    elapsedsecs = 0
    maxsecs = 3600 * watchoptions.maxdur
        
    # Loop to append to file every "tint" hours
    print("Starting loop to check prices every " + str(watchoptions.tint) + " hours")
    while (elapsedsecs < maxsecs):
        elapsedsecs = time.time() - time0
        
        with open(file_out, "a+") as fopen:  # get # of lines in price log
            oldnum_lines = sum(1 for line in fopen)
             
        # Check website for prices    
        grid_list = PyWestPricecheck.pricecheck(flightoptions)
        
        with open(file_out, "a") as fopen:  # Now write new-found prices to log
            fopen.write("Searched on:  " + time.strftime('%X %x') + "\n")            
            for row in grid_list:
                print(row)
                fopen.write(row + "\n")

        # Now read file for minimum price
        prices = []
        foundlines = []
        alllines = [[]]
        lookup = re.compile('[$](\d+(?:\.d{2})?)')  # regex format for a price: $*[.??] 
        with open(file_out, "a+") as fopen:  #  open for reading and appending 
            for line_num, line in enumerate(fopen, 1):
                # check if we have a regex match for a price:
                if lookup.search(line):
                    foundprice = re.findall(lookup, line)
                    prices.append(float(foundprice[0]))
                    foundlines.append(line_num)
                    #print(line_num, foundprice[0])
            minprice = min(prices) # get min price in log file
            mindex = prices.index(minprice)  # get index of min price
            minline = foundlines[mindex]  # get line number of min price
            #print(mindex, minprice)
            
            if minline > oldnum_lines:  # if the min price is the new lines
                print("FOUND NEW MINIMUM PRICE: $" + str(minprice))
                fopen.write("FOUND NEW MINIMUM PRICE: $" + str(minprice) + "\n")
                
                # Send email alerts:
                subjtext = "Flight " + foutname + ": New lowprice of $" + str(minprice)
                bodytext = ("""New minimum price for flight search {}
                    Details: Origin: {},  Dest: {} Date: {}
                        {}
                        {}
                        
                    This was found and sent by PyWestPriceWatcher
                    The price log file is at: {}  
                        """)
                        
                # foutname is short flight data, grid_list[0] is labels,
                # grid_list[mindex+1] should be the flight info of the min price                                 
                bodytext = bodytext.format(foutname, flightoptions.dest_port,
                                      flightoptions.origin_port, flightoptions.out_date,
                                      grid_list[0], grid_list[mindex + 1],
                                      socket.gethostname() + ":/" + file_out)
                # bodytext = bodytext.format(foutname,grid_list[0],grid_list[mindex+1],file_out)
                sendalert_yahoogmail(yahoologin, password, bodytext, subjtext, toaddrs)                
        time.sleep(3600 * watchoptions.tint)  # wait tint (in seconds)

    print("Max time elapsed. All done!")
    
    
if __name__ == "__main__":
    main()
