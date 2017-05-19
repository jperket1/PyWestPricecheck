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
#    [out_dir] [tint] [maxdur] [inifile]
# Requires: selenium, chromedriver (may be finicky on different systems)
#
# Todo: use invisible display for browser
# ---------------------------------------------------------------------------   

from ConfigParser import SafeConfigParser
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


# For inputs that won't change every run
def read_ini(inifile):
    parser = SafeConfigParser()
    # read last availbale file in list:
    parser.read(["./pywest_default.ini", "./pywest.ini", inifile])       
    pr={}
    
    for section_name in parser.sections():
        for name, value in parser.items(section_name):
            pr[name]=value
            
    return(pr)      
        
    
# A place for argparse stuff    
def watchinputs(): 
    parser = argparse.ArgumentParser(
         description="Periodically runs and monitors PyWestcheck while running \
                     in console. Sends an email alert when a new low price is found\
                     for the flights being searched for",
         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--out_dir", default='./', help="destination of log file (default = current dir)", required=False)    
    parser.add_argument("--tint", default=1, help="time interval in hours (default=1 hr)", required=False)    
    parser.add_argument("--maxdur", default=10, help="max duration to run in hours (default=10hr)", required=False)    
    parser.add_argument("--inifile", default="./pywest.ini", help="Config file. Won't send alerts and other stuff without it", required=False)    
    
    options = parser.parse_args()
    # FOR TESTING, REMOVE WHEN DONE
    #options = parser.parse_args("--out_dir ./ --tint 0.01 --maxdur 0.01 \
    #        --inifile ./pywest.ini".split() )
    options.maxdur=float(options.maxdur)
    options.tint=float(options.tint)
    
    return options


#===============================================================================
# Send an email alert. I made a throwaway yahoo email account for this
#===============================================================================
def sendalert_mail(pr, bodytext, subjtext,):
    
    fromaddr = pr["fromaddr"]
    msg = MIMEText(bodytext, _charset='utf-8')
    msg['Subject'] = Header(subjtext, 'utf-8')
    msg['From'] = fromaddr
    msg['To'] = pr["toaddrs"] 
     
    server = smtplib.SMTP(pr["smtp_server"], int(pr["smtp_port"]))
    server.starttls()
    server.login(pr["login"], pr["password"])
    server.sendmail(msg['From'], msg['To'], msg.as_string())    
    server.quit()      
    print("  Email sent!")

    
#===============================================================================
# Get info to search for flights ever [tint] hours, and logs retrievals.
# Checks if a new lower price has been retrieved. If so, emails an alert    
#===============================================================================
def main():    

# Read in arguments and vars: -------------------------------------------------- 
    wopts = watchinputs()  # get watcher command args
    fopts = PyWestPricecheck.flightinputs()  # get flight info command args
    try:
        wopts.inifile
    except NameError:
        print "Unable to find config file, won't send alerts and stuff"     
        pr =  read_ini('')
    else:
        print "Reading in config data" 
        pr =  read_ini(wopts.inifile)
        
        
    # email details to send new low price alerts:
    if pr["store_password"]:
        print "Using stored password"    
    else:        
        pr["password"] =getpass("Yahoo password :")
        
    # Create and open log file, if doesn't exist:
    foutname = fopts.origin_port + "." + fopts.dest_port + "." + fopts.out_date.replace("/", "-")
    file_out = os.path.abspath(wopts.out_dir + "/PyWestLog." + foutname + ".txt")
    
    # Init some timing stuff
    time0 = time.time()  # get current (Epoch) time 
    elapsedsecs = 0
    maxsecs = 3600 * wopts.maxdur        
        
# Loop to run every "tint" hours -----------------------------------------------
        
    print("Starting loop to check prices every " + str(wopts.tint) + " hours")
    while (elapsedsecs < maxsecs):
        elapsedsecs = time.time() - time0
        
        with open(file_out, "a+") as fopen:  # get # of lines in price log
            oldnum_lines = sum(1 for line in fopen)
             
        # Check website for prices    
        grid_list = PyWestPricecheck.pricecheck(fopts)
        
        with open(file_out, "a") as fopen:  # Now write new-found prices to log
            fopen.write("Searched on:  " + time.strftime('%X %x') + "\n")            
            for row in grid_list:
                print(row)
                fopen.write(row + "\n")

        # Now read file for minimum price
        prices = []
        foundlines = []
        
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
                bodytext = bodytext.format(foutname, fopts.dest_port,
                                      fopts.origin_port, fopts.out_date,
                                      grid_list[0], grid_list[mindex + 1],
                                      socket.gethostname() + ":/" + file_out)
                
                sendalert_mail(pr, bodytext, subjtext)
                                
        time.sleep(3600 * wopts.tint)  # wait tint (in seconds)

    print("Max time elapsed. All done!")
    
    
if __name__ == "__main__":
    main()
