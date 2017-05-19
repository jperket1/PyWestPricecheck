# ---------------------------------------------------------------------------   
# PyWestPricecheck.py - To check southwest flights (currently only one way)             
#     Usage: PyWestPricecheck.py [-t|--to] dest_port [-f|--from] origin_port
#     	     			 [-d|--outdate] "outbound date (MM/DD/YYYY)

# PyWestWatcher.py - Periodically runs and appends PyWestcheck output to log.  
#  		     Sends an email alert when a new low price is found
#     Usage: PyWestWatcher.py [-t|--to] dest_port [-f|--from] origin_port 
#     	     [-d|--outdate] "outbound date (MM/DD/YYYY)
#    	     [out_dir] [tint] [maxdur]

# Created by Justin <JustinPerket@gmail.com>                                          
# 2017-05-16                                                                    

# requires: selenium>=2.0,<=3.0, chromedriver
#
# Todo:                                                              
# More flight search customization, a config file                                           
# ---------------------------------------------------------------------------   
