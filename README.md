  

PyWestPricecheck searches Southwest's website for oneway, nonstop
    flights you specify, and returns the results
	 
	 Example: PyWestPricecheck.py --to DEN --from BOS --outdate 3/14/17

PyWestWatcher runs PyWestcheck at (roughly) regular intervals, and outputs
    the results to a log file. It prints out a message if a
    new lower price has been found, and emails you by default.

    This uses a custom config setting file, and will check flights every
    1 hour for 10 hours, and append output to a logfile in /path/to/logfile/
    that will be created if it doesn't exist.    
    
	 Example: PyWestWatcher.py  --to DEN --from BOS --outdate 3/14/17 \
	 	  --out_dir /path/to/logfile/ --tint 1 --maxdur 10 \
		  --inifile /dir/subdir/pywest.ini
		  
    Optional Arguments and Defaults:
    	 if not provided, these are the defaults:
	 --out_dir ./
	 --tint 1      (hours)
	 --maxdur 10   (hours)
	 --inifile ./pywest.ini, or --inifile ./pywest_default.ini


    Config File:
    	   This contains settings that are a pain to enter each time.
	   Right now it's just to set up the email alerts:

	   ./pywest_default.ini has:
  	   	   [email_alert]
		   send_alerts = true		     # will try to send email alerts
		   store_password = false      	     # will use password to send emails
		   fromaddr = foofrom@bar.com 	     # email address to send from
		   login = LOGIN	      	     # login associated with fromaddr
		   password = PASSWORD	    	     # password associated with fromaddr
		   smtp_server = smtp.mail.bar.com   
		   smtp_port = 587
		   toaddrs = footo@foo.com	     # email to send alerts to

	   If you want email alerts. you should save your settings in ./pywest.ini ,
	   or a file specified by --inifile
 	   
    	   In order of greater importance, PyWestWatcher will try to use:
	   ./pywest_default.ini , ./pywest.ini , file specified by --inifile
		  
		  		  


# ---------------------------------------------------------------------------   
PyWestPricecheck.py - To check southwest flights (currently only one way)             
    Usage: PyWestPricecheck.py [-t|--to] dest_port [-f|--from] origin_port
    	     			 [-d|--outdate] MM/DD/YYYY

PyWestWatcher.py - Periodically runs and appends PyWestcheck output to log.  
 		     Sends an email alert when a new low price is found
    Usage: PyWestWatcher.py [-t|--to] dest_port [-f|--from] origin_port 
    	     [-d|--outdate] "outbound date (MM/DD/YYYY)
   	     [--out_dir /path/to/logfile/] [--tint thours] [--maxdur dhours] [--inifile configfile]

Created by Justin <JustinPerket@gmail.com>                                          
2017-05-16                                                                    

requires: selenium>=2.0,<=3.0, chromedriver

Todo:                                                              
More flight search customization, make browser invisible                                           
---------------------------------------------------------------------------   
