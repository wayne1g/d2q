#! /usr/bin/env python
import sys
import argparse
import pytz
from datetime import datetime
from pprint import pprint

def d2q(*args):
    '''
    Expect a list of dictionary such as
    [{'date': '2016-11-25', 'tz': 'Asia/Hong_Kong'},
     ......,
     {'date': '2011-01-22', 'tz': 'US/Pacific'}]

     This function will add a couple more key/value pairs
     in the date and timezone dictionary;
     includes the quarter, and the datetime object base on the timezone given

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
    '''
    for item in args:
        # Define a naive datetime object base on the input date time string
        try:
            datetime_object = datetime.strptime(item['date'], '%Y-%m-%d')
        except ValueError as e:
            # Operations abort. Return error
            exit(e)
        # Convert naive datetime object to a timezone aware datetime object
        datetime_object = datetime_object.replace(tzinfo=pytz.timezone('UTC'))
        # Replace the tzinfo with the given time zone in the argument
        try:
            datetime_object = datetime_object.astimezone(pytz.timezone(item['tz']))
        except pytz.exceptions.UnknownTimeZoneError as e:
            # Operations abort. Return error
            exit(type(e)("Timezone value - " + e.message +\
                " does not match IANA requirement."))
        # except: # Catch all exception
        #     e = sys.exc_info()
        #     exit(e)
        # Add quarter to the dictionary
        item['quarter'] = quarter(datetime_object)
        # Add the datetime object to the dictionary
        item['dt_obj'] = datetime_object
    return args


def quarter(args):
    '''
    Expect a datetime object as argument to determine the relevant quarter
    month 1 to 3 is quarter 1,
    month 4 to 6 is quarter 2, etc
    '''
    quarter = (args.month - 1) // 3 + 1
    return quarter


if __name__ == '__main__':
    # Define arguments required
    p = argparse.ArgumentParser()
    p.add_argument('--date', nargs='+', \
        help = 'Date - E.g. 2016-12-25')
    p.add_argument('--tz', nargs='+', \
        help = 'IANA Date Time String - E.g. Asia/Hong_Kong, US/Pacific')
    # Generate a Namespace object from the parser
    args = p.parse_args()

    # Convert the content inside the Namesapce object into a dict
    # This dict contains 2 keys base on the arguments input.
    # 'date' and 'tz'; base on '--date' and '--tz'
    # E.g. {'date': ['2016-12-25'], 'tz': ['Asia/Hong_Kong']}
    kwargs = vars(args)

    # Detect missing input arguments.
    try:    # if either date or tz is not given (aka None), abort the program
        len(kwargs['tz'])
        len(kwargs['date'])
    except TypeError as e:
        # Operations abort. Return error
        exit(e)

    # Detect if we need to pad time zone
    # E.g. we have one time zone given for many dates to work with
    if len(kwargs['date']) > 1 and len(kwargs['tz']) == 1:
        # Pad tz until it is as long as date input
        for d in range(1, len(kwargs['date'])):
            kwargs['tz'].append(kwargs['tz'][0])

    # Make a list of dictionary as the input to the func
    arg_list = [{'date':kwargs['date'][i], 'tz':kwargs['tz'][i]} \
                for i in range(len(kwargs['date']))]
    # arg_list = []
    # for i in range(len(kwargs['date'])):
    #     arg_list.append({'date':kwargs['date'][i], 'tz':kwargs['tz'][i]})

    d2q(*arg_list)
