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
#    GTW.OMP.SWP.Clip
#
# Purpose
#    Model a news clip
#
# Revision Dates
#     9-Apr-2010 (CT) Creation
#    ��revision-date�����
#--

from   _GTW                   import GTW
from   _MOM.import_MOM        import *

import _GTW._OMP._SWP.Page

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SWP.Page

class _Clip_ (_Ancestor_Essence) :
    """News clip for the front page of a website."""

    is_partial = True

# end class _Clip_

_Ancestor_Essence = _Clip_

class Clip_I (_Ancestor_Essence) :
    """News clip for the front page of a website referring to an internal web
       page.
    """

# end class Clip_I

class Clip_X (_Ancestor_Essence) :
    """News clip for the front page of a website referring to an external web
       page.
    """

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class link_to (A_Url) :
            """Url of external web page providing information about this clip"""

            kind               = Attr.Optional

        # end class link_to

    # end class _Attributes

# end class Clip_X

_Ancestor_Essence = GTW.OMP.SWP.Link2

class Clip_to_Object (_Ancestor_Essence) :
    """News clip for a object."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """News clip"""

            role_type          = Clip_I
            role_name          = "clip"
            max_links          = 1

        # end class left

        class right (_Ancestor.right) :
            """Object the news clip refers to"""

            role_type          = GTW.OMP.SWP.Object_PN
            role_name          = "object"
            max_links          = 1
            auto_cache         = True

        # end class right

    # end class _Attributes

# end class Clip_to_Object

if __name__ != "__main__" :
    GTW.OMP.SWP._Export ("*")
### __END__ GTW.OMP.SWP.Clip
