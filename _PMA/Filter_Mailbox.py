# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Martin Gl�ck. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    PMA.Filter_Mailbox
#
# Purpose
#    A mailbox which does not contain real messages but presents a filtered
#    view of a mailbox (or a virtual mailbox).
#
# Revision Dates
#    23-Jan-2006 (MG) Creation
#    ��revision-date�����
#--

from   _PMA              import PMA
import _PMA.V_Mailbox
import  pdb

class Filter_Mailbox (PMA._V_Mailbox_) :
    """A mailbox which does not contain real messages but presents a filtered
       view of a mailbox (or a virtual mailbox).
    """

    def __init__ (self, name, matcher, mailbox, prefix = None, ** ckw) :
        self.mailboxes = (mailbox, )
        self.__super.__init__ \
            ( name     = name
            , prefix   = mailbox.qname
            , root     = mailbox.root
            )
        if not isinstance (matcher, PMA._Matcher_) :
            matcher          = PMA.Matcher (matcher, ** ckw)
        self._matcher        = matcher
    # end def __init__

    def _eligible (self, messages) :
        return self._matcher.filter (* messages)
    # end def _eligible

# end class Filter_Mailbox

"""
from _PMA                  import PMA
import _PMA.Mailbox
import _PMA.Filter_Mailbox
import _PMA.Matcher
import _PMA.Office

mb1 = PMA.Mailbox    ("/home/glueck/PMA/TTTech/planung")
mb2 = PMA.Mailbox    ("/home/glueck/PMA/TTTech/BIKA")
mbs = PMA.MH_Mailbox ("/home/glueck/work/MH/Installscript")
vmb = PMA.V_Mailbox  ("inboxes", (mb1, mb2))
fmb = vmb.add_filter_mailbox ("f1", "'maier' in sender or 'novak' in sender")
fmb.messages
m   = mbs.messages [58]
"""

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Filter_Mailbox
