# -*- coding: utf-8 -*-
# Copyright (C) 2010-2016 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.__test.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.__test.Event
#
# Purpose
#    Test SRM.Event and recurrence rules
#
# Revision Dates
#    18-Aug-2010 (CT) Creation
#    19-Aug-2010 (CT) Creation continued
#     6-Sep-2010 (CT) Adapted to change of Recurrence_Rule and Recurrence_Spec
#     7-Sep-2010 (CT) Tests for update of `Event_occurs` added
#     8-Sep-2010 (CT) Tests for Event without `Recurrence_Rule` added
#    15-Feb-2016 (CT) Add test for localized weekday names
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> EVT = scope.EVT
    >>> MOM = scope.MOM
    >>> SWP = scope.SWP
    >>> RR  = EVT.Recurrence_Rule
    >>> RS  = EVT.Recurrence_Spec

    >>> p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
    >>> p2 = SWP.Page ("event-2-text", text = "Text for the 2. event")

    >>> e1 = EVT.Event (p1.epk, dict (start = "2010-08-18", raw = True))
    >>> rs1 = RS (e1, date_exceptions = ["2010-08-15"])
    >>> rr1 = RR (rs1.epk_raw, start = "20100801", count = 7, unit = "Weekly", raw = True)
    >>> prepr (rr1.ui_display)
    '20100801, 20100808, 20100815, 20100822, 20100829, 20100905, 20100912'
    >>> prepr (rs1.ui_display)
    '20100801, 20100808, 20100822, 20100829, 20100905, 20100912'

    >>> prepr (tuple (evo.FO.date for evo in EVT.Event_occurs.query_s ()))
    ('2010-08-01', '2010-08-08', '2010-08-22', '2010-08-29', '2010-09-05', '2010-09-12')

    >>> x = e1.date.set_raw (finish = "2010-08-31")

    Now, `rs1` takes a default value for `until` from `e1.date.finish`
    >>> prepr (rs1.ui_display)
    '20100801, 20100808, 20100822, 20100829'
    >>> e1.dates
    [datetime.datetime(2010, 8, 1, 0, 0), datetime.datetime(2010, 8, 8, 0, 0), datetime.datetime(2010, 8, 22, 0, 0), datetime.datetime(2010, 8, 29, 0, 0)]
    >>> prepr (tuple (evo.FO.date for evo in EVT.Event_occurs.query_s ()))
    ('2010-08-01', '2010-08-08', '2010-08-22', '2010-08-29')

    >>> _ = rs1.set_raw (dates = ["2010-08-07", "2010-08-09"])
    >>> prepr (tuple (evo.FO.date for evo in EVT.Event_occurs.query_s ()))
    ('2010-08-01', '2010-08-07', '2010-08-08', '2010-08-09', '2010-08-22', '2010-08-29')

    >>> e2 = EVT.Event (p2)
    >>> e2.dates
    []
    >>> _ = e2.date.set (start = "2010-09-08")
    >>> e2.dates
    [datetime.datetime(2010, 9, 8, 0, 0)]
    >>> _ = e2.date.set (finish = "2010-09-09")
    >>> e2.dates
    [datetime.datetime(2010, 9, 8, 0, 0), datetime.datetime(2010, 9, 9, 0, 0)]
    >>> _ = e2.date.set (finish = "2010-09-12")
    >>> e2.dates
    [datetime.datetime(2010, 9, 8, 0, 0), datetime.datetime(2010, 9, 9, 0, 0), datetime.datetime(2010, 9, 10, 0, 0), datetime.datetime(2010, 9, 11, 0, 0), datetime.datetime(2010, 9, 12, 0, 0)]

    >>> rsx = RS (EVT.Event (p1))
    >>> def RR (** kw) :
    ...     for r in list (rsx.rules) : r.destroy ()
    ...     return EVT.Recurrence_Rule (rsx.epk_raw, raw = True, ** kw)

    >>> rr2 = RR (start = "20100801", count = 5, unit = "Daily", week_day = ("TU", "TH"))
    >>> prepr (rr2.ui_display)
    '20100803, 20100805, 20100810, 20100812, 20100817'

    >>> rr2a = RR (start = "20100801", count = 5, unit = "Daily", week_day = ("TH..MO"))
    >>> prepr (rr2a.ui_display)
    '20100801, 20100802, 20100805, 20100806, 20100807'

    >>> with TFL.I18N.test_language ("de") :
    ...     rr2_de = RR (start = "20100801", count = 5, unit = "Daily", week_day = ("Di", "Do"))
    ...     prepr (rr2_de.ui_display)
    '20100803, 20100805, 20100810, 20100812, 20100817'

    >>> rr3 = RR (start = "20100801", count = 5, unit = "Weekly", week_day = ("TU", "TH"))
    >>> prepr (rr3.ui_display)
    '20100803, 20100805, 20100810, 20100812, 20100817'

    >>> rr4 = RR (start = "20100801", count = 5, unit = "Daily", week_day = ("TU", "TH"), restrict_pos = "1")
    >>> prepr (rr4.ui_display)
    '20100803, 20100805, 20100810, 20100812, 20100817'

    >>> rr4a = RR (start = "20100801", count = 5, unit = "Daily", week_day = ("TU - TH"), restrict_pos = "1")
    >>> prepr (rr4a.ui_display)
    '20100803, 20100804, 20100805, 20100810, 20100811'

    >>> rr5 = RR (start = "20100801", count = 5, unit = "Weekly", week_day = ("TU", "TH"), restrict_pos = "1")
    >>> prepr (rr5.ui_display)
    '20100803, 20100810, 20100817, 20100824, 20100831'

    >>> rr6 = RR (start = "20100801", count = 5, unit = "Monthly")
    >>> prepr (rr6.ui_display)
    '20100801, 20100901, 20101001, 20101101, 20101201'

    >>> rr7 = RR (start = "20100831", count = 5, unit = "Monthly")
    >>> prepr (rr7.ui_display)
    '20100831, 20101031, 20101231, 20110131, 20110331'

    >>> rr8 = RR (start = "20100831", count = 5, unit = "Monthly", month_day = "-1")
    >>> prepr (rr8.ui_display)
    '20100831, 20100930, 20101031, 20101130, 20101231'

    >>> rr9 = RR (start = "20101231", count = 5, unit = "Monthly", month_day = "29, -1", restrict_pos = "1")
    >>> prepr (rr9.ui_display)
    '20110129, 20110228, 20110329, 20110429, 20110529'

    >>> rr10 = RR (start = "20100801", count = 5, period = 2, unit = "Daily")
    >>> prepr (rr10.ui_display)
    '20100801, 20100803, 20100805, 20100807, 20100809'

    >>> rr11 = RR (start = "20100801", count = 5, period = 10, unit = "Daily")
    >>> prepr (rr11.ui_display)
    '20100801, 20100811, 20100821, 20100831, 20100910'

    >>> rr12 = RR (start = "20100101", finish = "20120101", month = "1", week_day = "MO", unit = "Yearly")
    >>> prepr (rr12.ui_display)
    '20100104, 20100111, 20100118, 20100125, 20110103, 20110110, 20110117, 20110124, 20110131'

    >>> rr13 = RR (start = "20100801", count = 5, period = 2, unit = "Weekly", week_day = ("TU", "TH"))
    >>> prepr (rr13.ui_display)
    '20100810, 20100812, 20100824, 20100826, 20100907'

    >>> rr14 = RR (start = "20100801", count = 5, unit = "Monthly", week_day = "MO")
    >>> prepr (rr14.ui_display)
    '20100802, 20100809, 20100816, 20100823, 20100830'

    Monthly on the 1st Monday
    >>> rr15 = RR (start = "20100801", count = 5, unit = "Monthly", week_day = "MO(1)")
    >>> prepr (rr15.ui_display)
    '20100802, 20100906, 20101004, 20101101, 20101206'

    Every other month on the 1st and last Sunday of the month
    >>> rr16 = RR (start = "20100801", count = 5, period = 2, unit = "Monthly", week_day = "SU(1), SU(-1)")
    >>> prepr (rr16.ui_display)
    '20100801, 20100829, 20101003, 20101031, 20101205'

    Monthly on the fifth to the last day of the month,
    >>> rr17 = RR (start = "20101101", count = 5, unit = "Monthly", month_day = "-5")
    >>> prepr (rr17.ui_display)
    '20101126, 20101227, 20110127, 20110224, 20110327'

    Every 2nd year on the 1st, 100th and 200th day
    >>> rr19 = RR (start = "20100101", count = 6, period = 2, unit = "Yearly", year_day = "1,100, 200")
    >>> prepr (rr19.ui_display)
    '20100101, 20100410, 20100719, 20120101, 20120409, 20120718'

    Every 20th Monday of the year,
    >>> rr20 = RR (start = "20100101", count = 6, unit = "Yearly", week_day = "MO(20)")
    >>> prepr (rr20.ui_display)
    '20100517, 20110516, 20120514, 20130520, 20140519, 20150518'

    Monday of week number 20 (where the default start of the week is Monday),
    >>> rr21 = RR (start = "20100101", count = 6, unit = "Yearly", week = "20", week_day = "MO")
    >>> prepr (rr21.ui_display)
    '20100517, 20110516, 20120514, 20130513, 20140512, 20150511'

    The week number 1 may be in the last year.
    >>> rr22 = RR (start = "20100101", count = 6, unit = "Yearly", week = "1", week_day = "MO")
    >>> prepr (rr22.ui_display)
    '20100104, 20110103, 20120102, 20121231, 20131230, 20141229'

    And the week numbers greater than 51 may be in the next year.
    >>> rr23 = RR (start = "20100101", count = 6, unit = "Yearly", week = "52", week_day = "SU")
    >>> prepr (rr23.ui_display)
    '20120101, 20121230, 20131229, 20141228, 20151227, 20170101'

    Only some years have week number 53:
    >>> rr24 = RR (start = "20100101", count = 6, unit = "Yearly", week = "53", week_day = "MO")
    >>> prepr (rr24.ui_display)
    '20151228, 20201228, 20261228, 20321227, 20371228, 20431228'

    Every Friday the 13th,
    >>> rr25 = RR (start = "20100101", count = 6, unit = "Yearly", month_day = "13", week_day = "FR")
    >>> prepr (rr25.ui_display)
    '20100813, 20110513, 20120113, 20120413, 20120713, 20130913'

    Every four years, the first Tuesday after a Monday in November, (U.S. Presidential Election day):
    >>> rr26 = RR (start = "20080101", count = 6, period = 4, unit = "Yearly", month = "11", month_day = "2,3,4,5,6,7,8", week_day = "TU")
    >>> prepr (rr26.ui_display)
    '20081104, 20121106, 20161108, 20201103, 20241105, 20281107'

    The 3rd instance into the month of one of Tuesday, Wednesday or Thursday,
    >>> rr27 = RR (start = "20101101", count = 5, unit = "Monthly", week_day = "TU - TH", restrict_pos = "3")
    >>> prepr (rr27.ui_display)
    '20101104, 20101207, 20110106, 20110203, 20110303'

    The 2nd to last weekday of the month,
    >>> rr28 = RR (start = "20100701", count = 5, unit = "Monthly", week_day = "MO..FR", restrict_pos = "-2")
    >>> prepr (rr28.ui_display)
    '20100729, 20100830, 20100929, 20101028, 20101129'

    >>> RR  = EVT.Recurrence_Rule
    >>> rsy = RS (EVT.Event (p2))
    >>> rry = RR (rsy.epk_raw, start = "20100801", unit = "Daily", count = 7, raw = True)
    >>> rrz = RR (rsy.epk_raw, start = "20100801", unit = "Yearly", week_day = "SA,SU", is_exception = "yes", raw = True)
    >>> prepr (rsy.ui_display)
    '20100802, 20100803, 20100804, 20100805, 20100806'

    >>> prepr (A_Time_List.as_string (A_Time_List.from_string ("10:42")))
    '10:42'

    >>> prepr (A_Time_List.as_string (A_Time_List.from_string ("10:42-13:53")))
    '10:42,11:42,12:42,13:42'

    >>> prepr (A_Date_List.as_string (A_Date_List.from_string ("2016-04-28..2016-05-01")))
    '2016-04-28,2016-04-29,2016-04-30,2016-05-01'

    >>> prepr (A_Date_Time_List.as_string (A_Date_Time_List.from_string ("2016-04-28 10:00 - 2016-04-30 10:00")))
    '2016-04-28 10:00,2016-04-29 10:00,2016-04-30 10:00'

"""

from _GTW.__test__.model import *
import datetime

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test.Event
