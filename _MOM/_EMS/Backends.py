# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.EMS.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.EMS.Backends
#
# Purpose
#    Provide access to supported EMS/DBW backends
#
# Revision Dates
#    23-Jun-2010 (CT) Creation
#    ��revision-date�����
#--

"""
    >>> print MOM.EMS.Backends.get ("postgresql:")
    (<class '_MOM._EMS.SAS.Manager'>, <class '_MOM._DBW._SAS.Manager.Manager'>, <class '_MOM._DBW._SAS.DBS.Postgresql'>)
    >>> print MOM.EMS.Backends.get ("mysql:")
    (<class '_MOM._EMS.SAS.Manager'>, <class '_MOM._DBW._SAS.Manager.Manager'>, <class '_MOM._DBW._SAS.DBS.MySQL'>)
    >>> print MOM.EMS.Backends.get ("hps:")
    (<class '_MOM._EMS.Hash.Manager'>, <class '_MOM._DBW._HPS.Manager.Manager'>, <class '_MOM._DBW._HPS.DBS.HPS'>)

"""

from   _MOM                   import MOM
import _MOM._EMS

_hps = ("Hash", "_HPS.Manager")
_sas = ("SAS",  "_SAS.Manager")

Map  = dict \
    ( hps        = _hps
    , mysql      = _sas
    , postgresql = _sas
    , sqlite     = _sas
    , ** { ""    : _hps
         , None  : _hps
         }
    )

def get (url) :
    """Return (`EMS`, `DBW`) for `scheme` of `url`."""
    import _MOM._DBW
    if ":" not in url :
        raise ValueError ("`%s` doesn't contain a scheme" % url)
    scheme = url.split (":") [0]
    e, d   = Map [scheme]
    EMS    = MOM.EMS._Import_Module (e).Manager
    DBW    = MOM.DBW._Import_Module (d).Manager
    return (EMS, DBW, DBW.DBS_map [scheme])
# end def get

if __name__ != "__main__" :
    MOM.EMS._Export_Module ()
### __END__ MOM.EMS.Backends