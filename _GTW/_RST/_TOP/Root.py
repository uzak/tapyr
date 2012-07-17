# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.RST.TOP.Root
#
# Purpose
#    Root class of tree of pages
#
# Revision Dates
#     5-Jul-2012 (CT) Creation (based on GTW.NAV.Base)
#     9-Jul-2012 (CT) Add `static_handler`
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource
import _GTW._RST._TOP.Dir

from   _TFL._Meta.Once_Property import Once_Property

import _TFL._Meta.Object
import _TFL.defaultdict

import time

class TOP_Root (GTW.RST.TOP._Dir_, GTW.RST.Root) :
    """Root of tree of pages."""

    _real_name                 = "Root"

    Media_Parameters           = None

    copyright_start            = None
    copyright_url              = None
    owner                      = None
    q_prefix                   = "q"
    qx_prefix                  = "qx"
    translator                 = None

    _exclude_robots            = False
    _login_required            = False
    _static_handler            = None

    from _GTW._RST._TOP.Request  import Request  as Request_Type
    from _GTW._RST._TOP.Response import Response as Response_Type

    class E_Type_Desc (TFL.Meta.Object) :

        _admin   = None
        _manager = None

        @property
        def admin (self) :
            return self._admin
        # end def admin

        @admin.setter
        def admin (self, value) :
            if self._admin is None :
                self._admin = value
        # end def admin

        @property
        def manager (self) :
            return self._manager
        # end def manager

        @manager.setter
        def manager (self, value) :
            if self._manager is None :
                self._manager = value
        # end def manager

    # end class E_Type_Desc

    def __init__ (self, HTTP, ** kw) :
        self.pop_to_self (kw, "static_handler", prefix = "_")
        if "copyright_start" not in kw :
            kw ["copyright_start"] = time.localtime ().tm_year
        self.ET_Map = TFL.defaultdict (self.E_Type_Desc)
        self.__super.__init__ (HTTP = HTTP, ** kw)
    # end def __init__

    @classmethod
    def allow (cls, link, user) :
        try :
            allow_user = link.allow_user
        except Exception :
            return True
        else :
            return allow_user (user)
    # end def allow

    @Once_Property
    def home (self) :
        if self.dir_template is None :
            try :
                return first (self.own_links)
            except IndexError :
                pass
        return self
    # end def home

    @property
    def h_title (self) :
        return unicode (self.owner or self.name)
    # end def h_title

    @Once_Property
    def login_url (self) :
        if "Auth" in self.SC :
            return self.SC.Auth.href_login
    # end def login_url

    @Once_Property
    def static_handler (self) :
        result = self._static_handler
        if result is None :
            p = sos.path.normpath \
                (sos.path.join (sos.path.dirname (__file__), "../..", "media"))
            result = self._static_handler = self.HTTP.Static_File_App ("GTW", p)
        return result
    # end def static_handler

Root = TOP_Root # end class

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("*")
### __END__ GTW.RST.TOP.Root