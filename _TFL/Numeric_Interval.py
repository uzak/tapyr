# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003-2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Numeric_Interval
#
# Purpose
#    Model a numeric interval
#
# Revision Dates
#    18-Nov-2003 (CT) Creation
#    27-Nov-2003 (CT) `shifted` added
#    20-Feb-2004 (CT) `doctest` added
#    23-Feb-2004 (CT) `union`   added
#     4-Mar-2004 (CED) `difference` fixed
#     8-Mar-2004 (CED) Doctest fixed according to last change
#     9-Mar-2004 (CT)  `_doc_test` changed to not use `import`
#    ��revision-date�����
#--

from   _TFL                 import TFL

import _TFL.DL_List
import _TFL.predicate
import _TFL._Meta.Object

import sys

class Numeric_Interval (TFL.Meta.Object) :
    """Class for modelling a numeric interval.

       >>> i = Numeric_Interval (0, 100)
       >>> j = Numeric_Interval (100, 200)
       >>> k = Numeric_Interval (20, 50)
       >>> l = Numeric_Interval (210, 250)
       >>> m = Numeric_Interval (240, 260)
       >>> n = Numeric_Interval (280, 300)
       >>> i, j, k
       ((0, 100), (100, 200), (20, 50))
       >>> i.after (i), i.after (j), j.after (j), j.after (i)
       (False, False, False, True)
       >>> i.before (i), i.before (j), j.before (j), j.before (i)
       (False, True, False, False)
       >>> i.contains (i), i.contains (j), i.contains (k), j.contains (k)
       (True, False, True, False)
       >>> i.contains_point (100), i.contains_point (20), j.contains_point (20)
       (True, True, False)
       >>> i.difference (i), i.difference (j), i.difference (k)
       ([], [(0, 100)], [(0, 20), (50, 100)])
       >>> i.intersection (i), i.intersection (j), i.intersection (k)
       ((0, 100), (100, 100), (20, 50))
       >>> i.overlaps (i), i.overlaps (j), i.overlaps (k), j.overlaps (k)
       (True, False, True, False)
       >>> i.shifted (20)
       (20, 120)
       >>> i [0], i [1]
       (0, 100)
       >>> Numeric_Interval.union ()
       []
       >>> Numeric_Interval.union (m)
       [(240, 260)]
       >>> Numeric_Interval.union (i, k)
       [(0, 100)]
       >>> i, j, k, l, m, n
       ((0, 100), (100, 200), (20, 50), (210, 250), (240, 260), (280, 300))
       >>> Numeric_Interval.union (i, j, k, l, m, n)
       [(0, 200), (210, 260), (280, 300)]
    """

    format = "(%s, %s)"

    def __init__ (self, lower = sys.maxint, upper = - sys.maxint) :
        self.lower = lower
        self.upper = upper
    # end def __init__

    length = property (lambda s : s.upper - s.lower)

    def after (self, other) :
        return self.lower >= other.upper
    # end def after

    def before (self, other) :
        return self.upper <= other.lower
    # end def before

    def contains (self, other) :
        return self.lower <= other.lower <= other.upper <= self.upper
    # end def contains

    def contains_point (self, point) :
        return self.lower <= point <= self.upper
    # end def contains_point

    def copy (self) :
        return self.__class__ (self.lower, self.upper)
    # end def copy

    def difference (self, other) :
        result = []
        isect  = self.intersection (other)
        if isect :
            r = self.__class__ (self.lower, isect.lower)
            if r :
                result.append (r)
            r = self.__class__ (isect.upper, self.upper)
            if r :
                result.append (r)
        else :
            result = [self]
        return result
    # end def difference

    def intersection (self, other) :
        return self.__class__ \
            (max (self.lower, other.lower), min (self.upper, other.upper))
    # end def intersection

    def intersect (self, other) :
        self.lower = max (self.lower, other.lower)
        self.upper = min (self.upper, other.upper)
    # end def intersect

    def is_empty (self) :
        return self.lower == self.upper
    # end def is_empty

    def is_valid (self) :
        return self.lower <= self.upper
    # end def is_valid

    def overlaps (self, other) :
        return not (self.upper <= other.lower or self.lower >= other.upper)
    # end def overlaps

    def shift (self, delta) :
        self.lower += delta
        self.upper += delta
    # end def shift

    def shifted (self, delta) :
        return self.__class__ (self.lower + delta, self.upper + delta)
    # end def shifted

    def __cmp__ (self, other) :
        try :
            return cmp ((self.lower, self.upper), (other.lower, other.upper))
        except AttributeError :
            return cmp ((self.lower, self.upper), other)
    # end def __cmp__

    def __getitem__ (self, key) :
        return (self.lower, self.upper) [key]
    # end def __getitem__

    def __nonzero__ (self) :
        return self.length > 0
    # end def __nonzero__

    def __repr__ (self) :
        return self.format % (self.lower, self.upper)
    # end def __repr__

    def __setitem__ (self, key, value) :
        setattr (self, ("lower", "upper") [key], value)
    # end def __setitem__

    def union (cls, * args) :
        """Returns a list of intervals with the union of `args`"""
        result = []
        p      = TFL.DL_List \
            (* TFL.dusort (args, lambda i : (i.lower, i.upper))).head
        while p :
            pv = p.value
            q  = p.next
            while q and pv.upper >= q.value.lower :
                if pv.upper < q.value.upper :
                    pv = cls (pv.lower, q.value.upper)
                q = q.next
            result.append (pv)
            p = q
        return result
    union = classmethod (union)

# end class Numeric_Interval

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Numeric_Interval
