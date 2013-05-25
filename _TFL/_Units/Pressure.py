# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2013 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Units.Pressure
#
# Purpose
#    Units of pressure
#
# Revision Dates
#     8-Aug-2004 (CT) Creation
#    ��revision-date�����
#--

from   _TFL import TFL
import _TFL._Meta.Object
import _TFL._Units.Kind

class Pressure (TFL.Units.Kind) :
    """Units of pressure

       >>> Pressure (1.0)
       1
       >>> Pressure (1.0,"bar")
       100000
       >>> Pressure (1.0,"atm")
       101325
    """

    Unit              = TFL.Units.Unit

    base_unit         = Unit ("pascal", 1.0, "Pa")
    _units            = \
        ( ### see http://en.wikipedia.org/wiki/Conversion_of_units
        # Usual units
          Unit ("torr",                  133.3223684,     "torr")
        , Unit ("atmosphere",              1.01325E+5,    "atm")
        , Unit ("bar",                     1.0E+5,        "bar")
        # US customary units
        , Unit ("pound_per_square_foot",  47.880259,      "psf")
        , Unit ("pound_per_square_inch",   6.894757e3,    "psi")
        )

# end class Pressure

if __name__ != "__main__" :
    TFL.Units._Export ("*")
### __END__ TFL.Units.Pressure
