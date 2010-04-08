# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SWP.
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
#    GTW.OMP.SWP.Page
#
# Purpose
#    Model a static web page
#
# Revision Dates
#    31-Jan-2010 (CT) Creation
#     2-Feb-2010 (CT) Creation continued
#     9-Feb-2010 (CT) Creation continued..
#    24-Feb-2010 (CT) s/Lifetime/Date_Interval/
#    24-Feb-2010 (CT) `head_line` added
#     5-Mar-2010 (CT) `author.Class` set to class `GTW.OMP.PAP.Person`
#     5-Mar-2010 (CT) `Page.rank` defined, attribute `prio` added
#     7-Mar-2010 (CT) s/title/short_title/; s/description/title/
#    17-Mar-2010 (CT) `email_obfuscator` removed
#    22-Mar-2010 (CT) `Object_PN` factored
#    24-Mar-2010 (CT) `Page_Y` added
#     8-Apr-2010 (CT) `year_max` removed from `Page_Y` (was a bad idea (TM))
#    ��revision-date�����
#--

from   _MOM.import_MOM          import *
from   _MOM._Attr.Date_Interval import *

from   _GTW                     import GTW

import _GTW._OMP._SWP.Entity
from   _GTW._OMP._SWP.Format    import A_Format

from   _TFL.I18N                import _, _T, _Tn

import datetime

_Ancestor_Essence = GTW.OMP.SWP.Object_PN

class Page (_Ancestor_Essence) :
    """Model a static web page."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Non-primary attributes

        class contents (A_Text) :
            """Contents of web page in html format"""

            kind               = Attr.Internal
            auto_up_depends    = ("format", "text")

            def computed (self, obj) :
                return obj.format.convert (obj.text)
            # end def computed

        # end class contents

        class format (A_Format) :
            """Markup format used for `text` of web page"""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Sticky_Mixin, )
            default            = GTW.OMP.SWP.Format.ReST

        # end class format

        class head_line (A_String) :
            """Head line of the web page"""

            kind               = Attr.Optional
            max_length         = 120

        # end class head_line

        class prio (A_Int) :
            """Higher prio sorts before lower prio."""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Sticky_Mixin, )
            default            = 0

        # end class prio

        class text (A_Text) :
            """Text for web page in markup specified by `format`."""

            kind               = Attr.Mandatory

        # end class text

    # end class _Attributes

# end class Page

_Ancestor_Essence = Page

class Page_Y (_Ancestor_Essence) :
    """Model a year-specific static web page."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class year (A_Int) :
            """Year to which the web page applies."""

            kind               = Attr.Primary_Optional
            min_value          = 1986

        # end class year

    # end class _Attributes

# end class Page_Y

if __name__ != "__main__" :
    GTW.OMP.SWP._Export ("*")
### __END__ GTW.OMP.SWP.Page
