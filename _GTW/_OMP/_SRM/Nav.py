# -*- coding: utf-8 -*-
# Copyright (C) 2010-2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package  GTW.OMP.SRM.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#     GTW.OMP.SRM.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#    19-Apr-2010 (CT) Creation
#    30-Apr-2010 (MG) Adapted to new form's
#     2-May-2010 (MG) Simplified
#     6-May-2010 (MG) Switch to render mode rendering
#    31-Aug-2010 (CT) `Team` and `Team_has_Boat_in_Regatta` added
#     6-Sep-2010 (CT) `Boat_in_Regatta` adapted to change of `race_results`
#     7-Sep-2011 (CT) `Sailor` added
#    23-Sep-2011 (CT) `Club` added
#     7-Oct-2011 (CT) `GTW.OMP.SRM.Boat_in_Regatta.GTW.afs_spec` added
#    14-Nov-2011 (CT) Correct `Boat_in_Regatta.sort-key`
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    24-Jan-2012 (CT) Add `_crew` to `GTW.OMP.SRM.Boat_in_Regatta.GTW.afs_spec`
#    24-Jan-2012 (CT) Remove `Form_args`, `regatta_completer`,
#                     i.e., stuff related to non-AFS forms
#     1-Feb-2012 (CT) Add `Extra` "AF_BiR" to `Form_Cache`
#     2-Feb-2012 (CT) Add `attr_spec` parameters to `AF_BiR`
#    27-Feb-2012 (CT) Add `GTW.OMP.SRM.Club.GTW.afs_kw` (`collapsed = False`)
#     4-Jun-2012 (CT) Rename `handicap` to `boat_class`
#    26-Aug-2014 (CT) Replace `GTW.AFS` specification by `MF3_Form_Spec`
#    26-Sep-2014 (CT) Change `sail_number_x` from `skip` to `readonly`
#    30-Mar-2015 (CT) Add `Ranking`, `Regatta_in_Ranking`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _TFL                     import TFL
from   _GTW                     import GTW

from   _TFL.I18N                import _

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Boat               = dict \
        ( ETM          = "GTW.OMP.SRM.Boat"
        , sort_key     = TFL.Sorted_By ("left.name", "nation", "sail_number")
        )
    Boat_Class         = dict \
        ( ETM          = "GTW.OMP.SRM.Boat_Class"
        , sort_key     = TFL.Sorted_By ("name")
        )
    Boat_in_Regatta    = dict \
        ( ETM          = "GTW.OMP.SRM.Boat_in_Regatta"
        , sort_key     = TFL.Sorted_By
            ( "-regatta.event.date.start"
            , "skipper.person.last_name"
            , "skipper.person.first_name"
            )
        , MF3_Form_Spec        = dict
            ( include_rev_refs = ("_crew", "race_results")
            )
        , MF3_Attr_Spec_R      = dict
            ( { "left.left.max_crew"
                               : dict (skip       = True)
              , "left.sail_number_x"
                               : dict (readonly   = True)
              }
            , right            = dict (prefilled  = True)
            , place            = dict (skip       = True)
            , points           = dict (skip       = True)
            )
        , MF3_Form_Spec_R      = dict
            ( include_rev_refs = ("_crew", )
            )
        )
    Club               = dict \
        ( ETM          = "GTW.OMP.SRM.Club"
        )
    Page               = dict \
        ( ETM          = "GTW.OMP.SRM.Page"
        , sort_key     = TFL.Sorted_By ("-date.start", "perma_name")
        , list_display =
            ( "ui_display", "created_by", "date", "format", "last_changed")
        )

    Person_owns_Boat   = dict \
        ( ETM          = "GTW.OMP.SRM.Person_owns_Boat"
        )

    Ranking            = dict \
        ( ETM          = "GTW.OMP.SRM.Ranking"
        )

    Regatta_C          = dict \
        ( ETM          = "GTW.OMP.SRM.Regatta_C"
        , sort_key     = TFL.Sorted_By ("-event.date.start", "boat_class.name")
        , list_display = ("event", "boat_class", "kind")
        )

    Regatta_H          = dict \
        ( ETM          = "GTW.OMP.SRM.Regatta_H"
        , sort_key     = TFL.Sorted_By ("-event.date.start", "boat_class.name")
        , list_display = ("event", "boat_class", "kind")
        )

    Regatta_Event      = dict \
        ( ETM          = "GTW.OMP.SRM.Regatta_Event"
        , sort_key     = TFL.Sorted_By ("-date.start", "name")
        , list_display = ( "name", "date", "desc")
        )

    Regatta_in_Ranking            = dict \
        ( ETM          = "GTW.OMP.SRM.Regatta_in_Ranking"
        )

    Sailor             = dict \
        ( ETM          = "GTW.OMP.SRM.Sailor"
        )

    Team               = dict \
        ( ETM          = "GTW.OMP.SRM.Team"
        , sort_key     = TFL.Sorted_By
            ( "-regatta.event.date.start"
            , "name"
            )
        , list_display = ("regatta", "name", "club", "leader")
        )

    Team_has_Boat_in_Regatta = dict \
        ( ETM          = "GTW.OMP.SRM.Team_has_Boat_in_Regatta"
        , list_display = ("team", "boat.boat")
        )

# end class Admin

if __name__ != "__main__" :
     GTW.OMP.SRM._Export_Module ()
### __END__  GTW.OMP.SRM.Nav
