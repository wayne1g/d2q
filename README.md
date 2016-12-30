# d2q
Convert a date string to a dictionary with quarter value and timezone and generate a proper datetime object.

usage: d2q.py [-h] [--date DATE [DATE ...]] [--tz TZ [TZ ...]]

Generate a dictionary from the given date string and the time zone. The
dictionary will contain the quarter of the date, and is also a timezone aware
datetime object.

optional arguments:
  -h, --help            show this help message and exit
  
  --date DATE [DATE ...]
                        Date - E.g. 2016-12-25
                        
  --tz TZ [TZ ...]      IANA Date Time String - E.g. Asia/Hong_Kong,
                        US/Pacific

This script expects to receive a list of dictionaries such as
    [{'date': '2016-11-25', 'tz': 'Asia/Hong_Kong'},
     ......,
     {'date': '2011-01-22', 'tz': 'US/Pacific'}]

It will add a couple more key/value pairs in the given date and timezone dictionary; this includes the quarter, and the datetime object base on the timezone given

     The format of 'date' is '2016-12-25' (i.e. '%Y-%m-%d').
     The format of 'tz' is base on IANA defintion and is case sensitive.
         E.g. 'Asia/Hong_Kong'
         You may find the timezones to be used here.
            pytz.all_timezones

Example of the output.
    ({'date': '2016-11-25',
      'dt_obj': datetime.datetime(2016, 11, 25, 8, 0,
                tzinfo=<DstTzInfo 'Asia/Hong_Kong' HKT+8:00:00 STD>),
      'quarter': 4,
      'tz': 'Asia/Hong_Kong'},
      ......,
     {'date': '2011-01-22',
     'dt_obj': datetime.datetime(2011, 1, 21, 16, 0,
               tzinfo=<DstTzInfo 'US/Pacific' PST-1 day, 16:00:00 STD>),
     'quarter': 1,
     'tz': 'US/Pacific'})
     
Runs the script in a shell.
$ python d2q.py --date 2016-12-25 2015-1-23  --tz 'Asia/Hong_Kong' 'US/Pacific'
({'date': '2016-12-25',
  'dt_obj': datetime.datetime(2016, 12, 25, 0, 0, tzinfo=<DstTzInfo 'Asia/Hong_Kong' HKT+8:00:00 STD>),
  'quarter': 4,
  'tz': 'Asia/Hong_Kong'},
 {'date': '2015-1-23',
  'dt_obj': datetime.datetime(2015, 1, 23, 0, 0, tzinfo=<DstTzInfo 'US/Pacific' PST-1 day, 16:00:00 STD>),
  'quarter': 1,
  'tz': 'US/Pacific'})
