# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    TOM.TKT.Tk.__init__
#
# Purpose
#    Package providing Tk toolkit support for TOM
#
# Revision Dates
#    14-Dec-2004 (CT) Creation
#    ��revision-date�����
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _TOM                   import TOM
import _TOM._TKT

Tk = Package_Namespace ()
TOM.TKT._Export ("Tk")

import _TOM._UI
TOM.UI.set_TKT (Tk)

del Package_Namespace

### __END__ TOM.TKT.Tk.__init__
