# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    Plan
#
# Purpose
#    Model a yearly calendar with appointments
#
# Revision Dates
#    13-Apr-2003 (CT) Creation
#    17-Apr-2003 (CT) `seq_generator` added to `PDF_Plan` to get correct
#                     sequence for printed calendar when cut
#    18-Apr-2003 (CT) `PDF_Plan` factored into separate module
#    19-Apr-2003 (CT) `_add_appointment` added
#     4-May-2003 (CT) Option `-Show` added
#     4-May-2003 (CT) `_date_time` factored
#     4-May-2003 (CT) `_day_generator` corrected (check year)
#     4-May-2003 (CT) Pattern for `weekday` added
#    11-Jan-2004 (CT) `holidays_too` added
#     6-Feb-2004 (CT) Use (y, m, d) tuples instead of strings as dictionary
#                     keys (for `Y.map`)
#    ��revision-date�����
#--

from   __future__            import generators

from   _TFL                  import TFL
from   _TFL._CAL             import CAL
from   _TFL._CAL.Appointment import prio_pat, time_pat
from   Date_Time             import *
from   Filename              import *
from   predicate             import *
from   Regexp                import *

import sos
import _TFL._Meta.Object
import _TFL._CAL.Appointment
import _TFL._CAL.Year

day_sep       = Regexp ("^#", re.M)
day_pat       = Regexp (r"^ (?P<day>\d{4}/\d{2}/\d{2}) ")
app_date_pat  = Regexp \
    ( r"(?P<date>"
        r"(?:"
          r"(?:"
            r"(?P<day> -? \d{1,2}) \."
            r"(?: (?P<month> \d{1,2}) \."
            r"  (?: (?P<year> \d{4}))?"
            r")?"
          r")"
          r"|"
          r"(?:"
            r"(?P<weekday> Mon|Tue|Wed|Thu|Fri|Sat|Sun)"
            r"(?: [.#] (?P<week> [0-5]?\d))?"
          r")"
        r")"
        r"[ ]+"
      r")?"
    , re.VERBOSE
    )
app_pat       = Regexp \
    ( app_date_pat.pattern
    + r"(?P<repeat> "
    +   r"\+ (?P<delta> \d+) (?P<unit> d|w|m)? "
    +   r"(?: [ ]* \* (?P<how_often> \d+))?"
    +   r"[ ]+"
    + r")?"
    + time_pat.pattern                  + r"?"
    + r"(?: [ ]* = " + prio_pat.pattern + r")?"
    + r"[ ]+"
    + r"(?P<activity> .+)"
    , re.VERBOSE
    )

def _day_generator (pat_match, day, month, year, Y) :
    delta     = int (pat_match.delta     or 0)
    how_often = int (pat_match.how_often or 1)
    unit      = pat_match.unit or ["d", "w"] [bool (pat_match.weekday)]
    if unit == "w" :
        delta *= 7
    elif unit == "m" and day < 0 :
        delta  = - delta
    for i in range (how_often) :
        d = day
        if day < 0 :
            d = Y.months [month - 1].days [day].number
        D = Y.dmap.get ((year, month, d))
        if not D :
            raise StopIteration
        yield D
        if unit == "m" :
            month += delta
        else :
            D = D.date + delta
            day, month = D.day, D.month
            if D.year != year :
                raise StopIteration
# end def _day_generator

def _date_time (Y, pat_match) :
    if pat_match.date or pat_match.time :
        today = Date ()
        if pat_match.weekday :
            wd = pat_match.weekday.lower ()
            wk = int (pat_match.week or today.week)
            d  = getattr (Y.weeks [wk - Y.weeks [0].number], wd).date
            if (pat_match.week is None) and d.julian_day < today.julian_day :
                d += 7
            day   = d.day
            month = d.month
            year  = d.year
        else :
            day   = int  (pat_match.day   or today.day)
            month = int  (pat_match.month or today.month)
            year  = int  (pat_match.year  or today.year)
        time  = pat_match.time or ""
        if time :
            if pat_match.hh_head :
                hh   = int (pat_match.hh_head)
                mm   = int (pat_match.mm_head or 0)
                time = "%2.2d:%2.2d" % (hh, mm)
                if pat_match.hh_tail :
                    hh   = int (pat_match.hh_tail)
                    mm   = int (pat_match.mm_tail or 0)
                    time = "%s-%2.2d:%2.2d" % (time, hh, mm)
        return day, month, year, time
    else :
        raise ValueError, "`%s` must specify either date or time"
# end def _date_time

def _add_appointment (Y, pat_match, holidays_too) :
    day, month, year, time = _date_time (Y, pat_match)
    app = ( CAL.Appointment.format
          % (time, pat_match.prio or " ", pat_match.activity)
          )
    for D in _day_generator (pat_match, day, month, year, Y) :
        if D.is_holiday and not holidays_too :
            continue
        D.add_appointments (* CAL.appointments (app))
# end def _add_appointment

def read_plan (Y, plan_file_name) :
    """Read information from file named `plan_file_name` and put appointments
       into `Y`
    """
    f = open (plan_file_name)
    try :
        buffer = f.read ()
    finally :
        f.close ()
    for entry in day_sep.split (buffer) :
        if day_pat.match (entry) :
            id = tuple ([int (f) for f in day_pat.day.split ("/")])
            d  = Y.dmap [id]
            head, tail = (entry.split ("\n", 1) + [""]) [:2]
            if tail :
                d.add_appointments (* CAL.appointments (tail))
# end def read_plan

def write_plan (Y, plan_file_name, replace = 0) :
    today = Date ()
    tail  = today.formatted ("%d.%m.%Y.%H:%M")
    if replace :
        sos.rename (plan_file_name, "%s-%s" % (plan_file_name, tail))
    else :
        plan_file_name = "%s.%s" % (plan_file_name, tail)
    CAL.write_year (Y.as_plan, plan_file_name, force = replace)
# end def write_plan

def _command_spec (arg_array = None) :
    from Command_Line import Command_Line
    today    = Date ()
    year     = today.year
    return Command_Line \
        ( option_spec =
            ( "add_appointment:B?Add appointments specified by arguments"
            , "diary:S=~/diary?Path for calendar file"
            , "filename:S=plan?Filename of plan for `year`"
            , "holidays_too:B?Add appointments to holidays, too"
            , "replace:B?Replace old calendar with new file"
            , "Show:B?Show days corresponding to arguments"
            , "sort:B?Sort calendar and write it back"
            , "year:I=%d?Year for which to process calendar" % (year, )
            )
        , description =
          """Manage appointments/activities in a yearly calendar.

             The arguments specify appointments. Examples of arguments:

             '7.1. +1w*52 14:30-15 =j SW-Jour-Fixe'
             '21.6. +1*8 =V Vacation'

             Argument syntax:

             <DD>.<MM>. +<delta><unit>*<how_often>
                 <hh>:<mm>-<hh>:<mm> =<Prio> <Activity/Appointment>

             Date, repeat-info, time, and priority are all optional, but at
             least one field of date or time must be specified. Missing date
             fields are replaced by the current day/month.

             The delta-unit can be specified as `d` for days (default), `w`
             for weeks, or `m` for months.

             The priority is a single letter (upper or lowercase) or number.
          """
        , arg_array   = arg_array
        )
# end def _command_spec

def _main (cmd) :
    year      = cmd.year
    path      = sos.path.join (sos.expanded_path (cmd.diary), "%4.4d" % year)
    Y         = CAL.Year      (year)
    file_name = sos.path.join (path, cmd.filename)
    sort      = cmd.sort
    read_plan   (Y, file_name)
    if cmd.add_appointment :
        sort  = len (cmd.argv)
        for a in cmd.argv :
            if app_pat.match (a.strip ()) :
                _add_appointment (Y, app_pat, cmd.holidays_too)
            else :
                print "%s doesn't match an appointment" % a
    if cmd.Show :
        for a in cmd.argv :
            if app_pat.match (a.strip ()) :
                print a
                pat_match = app_pat
                day, month, year, time = _date_time (Y, pat_match)
                for D in _day_generator (pat_match, day, month, year, Y) :
                    print "   ", D
            else :
                print "%s doesn't match an appointment" % a
    if sort :
        Y.sort_appointments ()
        write_plan (Y, file_name, cmd.replace)
# end def _main

if __name__ == "__main__" :
    _main (_command_spec ())
else :
    TFL.CAL._Export ("*")
### __END__ Plan
