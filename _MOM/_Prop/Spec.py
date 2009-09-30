# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Prop.Spec
#
# Purpose
#    Base class for attribute and predicate specification
#
# Revision Dates
#    30-Sep-2009 (CT) Creation (factored from TOM.Property_Spec)
#    ��revision-date�����
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Meta.M_Prop_Spec
import _MOM._Prop

import _TFL._Meta.Object

class _Prop_Spec_ (TFL.Meta.Object) :
    """Base class for attribute and predicate specification."""

    __metaclass__  = MOM.Meta.M_Prop_Spec
    _real_name     = "Spec"
    _prop_dict_cls = dict

    _mixed_kinds   = dict ()

    def __init__ (self, e_type) :
        self._create_prop_dict  (e_type)
        self._create_properties (e_type)
    # end def __init__

    def _add_prop (self, e_type, name, prop_type) :
        kind = self._effective_prop_kind (name, prop_type)
        if kind is not None :
            prop = self._new_prop (name, kind, prop_type, e_type)
            self._setup_prop      (e_type, name, kind.kind, prop)
            return prop
        else :
            setattr (e_type, name, None)
    # end def _add_prop

    def _create_prop_dict (self, e_type) :
        self._prop_dict = self._prop_dict_cls ()
        self._prop_kind = dict ((k, []) for k in pkg.Kind.Table)
        for n, v in self._prop_kind.iteritems () :
            setattr (e_type, self._kind_list_name (n), v)
    # end def _create_prop_dict

    def _create_properties (self, e_type) :
        ### TOM explicitly handled inherited properties here
        ### hope we don't need that anymore
        for n, prop_type in self._own_names.iteritems () :
            if prop_type is not None :
                self._add_prop (e_type, n, prop_type)
    # end def _create_properties

    def _effective_prop_kind (self, name, prop_type) :
        kind = result = getattr (prop_type, "kind",        None)
        kind_mixins   = getattr (prop_type, "Kind_Mixins", [])
        if kind is not None and kind_mixins :
            kinds = tuple (kind_mixins) + (kind, )
            try :
                result = self._mixed_kinds [kinds]
            except KeyError :
                result = self._mixed_kinds [kinds] = kind.__class__ \
                    ( "__".join (k.__name__ for k in reversed (kinds))
                    , kinds
                    , dict (__module__ = kind.__module__)
                    )
        return result
    # end def _effective_prop_kind

    def _kind_list_name (self, kind) :
        return kind
    # end def _kind_list_name

    def _new_prop (self, name, kind, prop_type, e_type) :
        return kind (prop_type)
    # end def _new_prop

    def _setup_prop (self, e_type, name, kind, prop) :
        self._prop_dict [name] = prop
        self._prop_kind [kind].append (prop)
        setattr (e_type, name, prop)
    # end def _setup_prop

Spec = _Prop_Spec_ # end class

if __name__ != "__main__" :
    MOM.Prop._Export ("*")
### __END__ MOM.Prop.Spec
