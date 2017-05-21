=========================================================================== 
PyWestPricecheck: A simple Southwest flight searcher and tracker
=========================================================================== 


:Purpose:   Mostly this is for me to learn Python. But also because Southwest isn't on most price-tracking websites.
:Requires: selenium, chromedriver
:Author: Justin  (JustinPerket@gmail.com)
:Date: 2017-05-16                                                                    
:References: (i.e., things I copied) Lots of stackoverflow,  Southwest-Checkin_

 .. _Southwest-Checkin: https://github.com/daveharmon/Southwest-Checkin



---------

Includes:
=========
**PyWestPricecheck** 

    Searches Southwest's website for oneway, nonstop flights you specify, and returns the results

**PyWestWatcher** 

    Runs PyWestcheck at (roughly) regular intervals, and outputs the results to a log file.
    It prints out a message if a new lower price has been found, and emails you by default.

**pyflight_default.ini**

    This contains settings that are a pain to enter each time. Right now it's just to set up the email alerts. Enter your email settings here, and rename to ``pyflight.ini``

|

---------

Use and options:
================

PyWestPricecheck
----------------

   **Usage**:
   
   .. code-block:: bash 
    
       PyWestPricecheck.py [-t|--to] $DST [-f|--from] $ORG [-d|--outdate] $DATE
   
   
   **Options**:
   
      -t <DST>, --to <DST>     To destination airport 
      -f <ORG>, --from <ORG>   From origin airport
      -d <DATE>, --outdate <DATE>   Date of flight
           

 
      Here, ``<DST>`` and ``<ORG>`` are the respective 3-letter codes_ for the destination and origin airports, and ``<DATE>`` is in the format MM/DD/YYYY [1]_.


.. _codes: http://en.wikipedia.org/wiki/International_Air_Transport_Association_airport_code

   
  **Example**: This will search for nonstop flights from Milwaukee to Denver on March 14, 2017:

  .. code-block:: bash 

    PyWestPricecheck.py --to DEN --from BOS --outdate 03/14/17
        
        
PyWestWatcher
-------------

  **Usage**:
   
  .. code-block:: sh  
    
    PyWestWatcher.py [-t|--to] $DST [-f|--from] $ORG \
              [-d|--outdate] $DATE \
              [--out_dir <dir>] [--tint <nhours1>] [--maxdur <nhours2>] [--inifile $inifile]
              
   
   
  **Options**
      
      *Required*
        
       (Same options as PyWestPricecheck)   
      
       -t <DST>, --to <DST>     To destination airport 
       -f <ORG>, --from <ORG>   From origin airport
       -d <DATE>, --outdate <DATE>   Date of flight

            
      *Optional*   [default]
        
       --out_dir <dir>       Outputs log file to directory <dir> [./]
       --tint <nhours1>      Checks flight data ever <nhours1> [1]
       --maxdur <nhours2>    Checks flights for a max of <nhours2> [10]
       --inifile <file.ini>  Loads config settings from <file.ini> [./pywest.ini]
       
  **Example**:     This will check flights every 1 hour for 10 hours, append output to a logfile in /path/to/logfile/ that will be created if it doesn't exist, and use a custom config setting file:

  .. code-block:: sh 

      PyWestWatcher.py  --to CHI --from BOS --outdate 3/14/17 \
        --out_dir /path/to/logfile/ --tint 1 --maxdur 10 \
        --inifile ./dir/subdir/pywest.ini
         
|

-------------

Config File
-----------

   This contains settings that are a pain to enter each time. Right now it's just to set up the email alerts:

   ``./pywest_default.ini`` has:

      .. code-block:: ini      
      
         [email_alert]
         send_alerts = true                 ; will try to send email alerts
         store_password = false             ; will use password to send emails
         fromaddr = foofrom@bar.com         ; email address to send from
         login = LOGIN                      ; login associated with fromaddr
         password = PASSWORD                ; password associated with fromaddr
         smtp_server = smtp.mail.bar.com    ; smpt server of fromaddr
         smtp_port = 587                    ; port of smpt server 
         toaddrs = footo@foo.com            ; email to send alerts to


   In order of increasing importance, PyWestWatcher will try to use:

      #)   ``./pywest_default.ini`` 
      #)   ``./pywest.ini``
      #)   ``<file.ini>`` specified by ``--inifile``
      
   If you want email alerts. you should save your settings as ./pywest.ini , or a file specified by ``--inifile``

|

-------
    
.. [1] Or whatever Southwest's website will accept, if you're feeling lucky  
    