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
#    GTW.RST.TOP.Dir
#
# Purpose
#    Model a directory in a tree of pages
#
# Revision Dates
#     6-Jul-2012 (CT) Creation (based on GTW.NAV.Base)
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource
import _GTW._RST._TOP.Base

from   _TFL._Meta.Once_Property import Once_Property

class _TOP_Dir_Base_ (GTW.RST.TOP._Base_, GTW.RST._Dir_Base_) :

    _real_name                 = "_Dir_Base_"

    def is_current_dir (self, page) :
        return page.prefix.startswith (self.prefix)
    # end def is_current_dir

_Dir_Base_ = _TOP_Dir_Base_ # end class

_Ancestor = _Dir_Base_

class _TOP_Dir_ (_Ancestor, GTW.RST._Dir_) :

    _real_name                 = "_Dir_"

    @property
    def has_children (self) :
        try :
            first (self.own_links)
        except IndexError :
            return False
        else :
            return True
    # end def has_children

    @property
    def own_links (self) :
        return iter (self.entries)
    # end def own_links

    @property
    def own_links_transitive (self) :
        for e in self.own_links :
            yield e
            if isinstance (e, _Dir_) :
                for ee in e.own_links_transitive :
                    yield ee
    # end def own_links_transitive

    @property
    def _effective (self) :
        dt = self.dir_template
        if dt is None :
            try :
                page = first (self.entries)
            except IndexError :
                pass
            else :
                return page._effective
        return self
    # end def _effective

_Dir_ = _TOP_Dir_ # end class

class TOP_Dir (_Dir_, GTW.RST.Dir) :
    """Directory of tree of pages."""

    _real_name                 = "Dir"

Dir = TOP_Dir # end class

class TOP_Dir_V (_Dir_Base_, GTW.RST.Dir_V) :
    """Volatile directory of tree of pages (directory with children,
       without permanent `_entries`).
    """

    _real_name                 = "Dir_V"

Dir_V = TOP_Dir_V # end class

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("*", "_Dir_Base_", "_Dir_")
### __END__ GTW.RST.TOP.Dir
