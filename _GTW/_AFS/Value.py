# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.
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
#    GTW.AFS.Value
#
# Purpose
#    Model the value of an element of a AFS form
#
# Revision Dates
#     1-Mar-2011 (CT) Creation
#     2-Mar-2011 (CT) Creation continued
#     5-Mar-2011 (CT) Creation continued..
#     8-Mar-2011 (CT) `apply` added
#     9-Mar-2011 (CT) `as_json_cargo` and `kw` added
#    10-Mar-2011 (CT) `apply` changed to iterate over `self.entities`
#     6-Apr-2011 (CT) `apply` changed to call `e.apply`, too
#     6-Apr-2011 (CT) `from_json` changed to except a dict as cargo, too
#    27-May-2011 (CT) `role_id` added
#    27-May-2011 (CT) `__repr__` added
#     1-Aug-2011 (CT) `edit` changed to test `is None` instead of truthyness of
#                     `._edit` (to allow setting attribute [raw] values to "")
#     2-Aug-2011 (CT) Message passed to `Error.Unknown` changed
#    20-Jan-2012 (CT) Add and use `_check_sids`
#     1-Mar-2012 (CT) Change `apply` to accumulate `results` and pass
#                     `results` to `elem.apply`
#     5-Mar-2012 (CT) Add `allow_new` to `pop_to_self`
#    12-Apr-2012 (CT) Add `errors` and `on_error` to `apply`
#    18-Apr-2012 (CT) Change `apply` to use `MOM.Error.as_json_cargo`, break
#                     on `MOM.Error.Error`
#    27-Apr-2012 (CT) Factor `record_errors`, change apply to
#                     `e.errors.append (exc)` if necessary
#     4-May-2013 (CT) Change `apply` to save `entity_values`
#    ��revision-date�����
#--

from   __future__  import unicode_literals, absolute_import

from   _GTW                     import GTW
from   _MOM                     import MOM
from   _TFL                     import TFL

import _GTW._AFS.Element
import _GTW._AFS.Error
from   _GTW._AFS.Instance       import _Base_

import _MOM.Error

import _TFL.Sorted_By
import _TFL._Meta.Property
from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.I18N                import _
from   _TFL.predicate           import uniq

import json

class Value (_Base_) :
    """Model the value of an AFS form element."""

    apply_key     = TFL.Sorted_By ("elem.rank", "-id")
    asyn          = None
    conflicts     = 0
    entity        = None
    prefilled     = None
    role_id       = None
    sid           = None
    value         = None
    _edit         = None
    _init         = None

    def __init__ (self, form, id, json_cargo) :
        self.form     = form
        self.id       = id
        self.jc       = json_cargo
        self.elem     = self._get_elem (form, id)
        self.children = children = []
        self.pop_to_self \
            ( json_cargo
            , "allow_new", "anchor_id", "edit", "init"
            , "prefilled", "role_id", "sid"
            )
        for c_id in sorted (uniq (json_cargo.get ("$child_ids", ()))) :
            children.append (self.__class__ (form, c_id, json_cargo [c_id]))
    # end def __init__

    @classmethod
    def from_json (cls, json_data) :
        if isinstance (json_data, basestring) :
            cargo = json.loads (json_data)
        else :
            cargo = json_data
        id    = cargo ["$id"]
        form  = cls._get_elem (GTW.AFS.Element.Form, id)
        return cls (form, id, cargo)
    # end def from_json

    @Once_Property
    def as_json_cargo (self) :
        result = self.__super.as_json_cargo
        result ["$id"] = self.elem.id
        return result
    # end def as_json_cargo

    @Once_Property
    def changed (self) :
        return self.init != self.edit
    # end def changed

    @Once_Property
    def changed_children (self) :
        return sum (c.changed for c in self.children)
    # end def changed_children

    @Once_Property
    def changes (self) :
        return self.changed + self.changed_children
    # end def changes

    @Once_Property
    def changes_t (self) :
        return self.changed + sum (c.changes_t for c in self.children)
    # end def changes_t

    @property
    def edit (self) :
        result = self._edit
        if result is None :
            result = self.init
        return result
    # end def edit

    @edit.setter
    def edit (self, value) :
        self._edit = value
    # end def edit

    @property
    def init (self) :
        result = self._init
        if result is None :
            result = self.elem.init
        if isinstance (result, str) :
            result = unicode (result)
        return result
    # end def init

    @init.setter
    def init (self, value) :
        self._init = value
    # end def init

    @Once_Property
    def kw (self) :
        def _gen () :
            if self.init :
                yield "init", self.init
            if self.changes :
                yield "edit", self.edit
            if self.asyn :
                yield "asyn", self.asyn
        # end def _gen
        result = dict (value = dict (_gen ()))
        return result
    # end def kw

    def apply (self, * args, ** kw) :
        conflicts = 0
        do_break  = False
        entities  = self.entity_values = sorted \
            (self.entity_children (), key = self.apply_key)
        results   = self.results  = {}
        errors    = self.errors   = {}
        self._check_sids   (entities, ** kw)
        for e in entities :
            e.errors = []
            try :
                e.entity = results [e.id] = e.elem.apply \
                    (e, results, * args, on_error = e.errors.append, ** kw)
            except MOM.Error.Error as exc :
                if not e.errors :
                    e.errors.append (exc)
                do_break = True
            self.record_errors (e)
            conflicts += e.conflicts
            if do_break :
                break
        if conflicts :
            raise GTW.AFS.Error.Conflict ()
    # end def apply

    def record_errors (self, e) :
        if e.errors :
            self.errors [e.id] = e.errors = MOM.Error.as_json_cargo (* e.errors)
    # end def record_errors

    def _check_sids (self, entities, ** kw) :
        for e in entities :
            e.elem.check_sid (e, ** kw)
    # end def _check_sids

    def _child_sig_iter (self, c, cig) :
        yield cig
    # end def _child_sig_iter

    @TFL.Meta.Class_and_Instance_Method
    def _get_elem (soc, form, id) :
        try :
            return form [id]
        except KeyError :
            raise GTW.AFS.Error.Unknown \
                (_ ("Form/element is unknown (unknown id: %s)") % (id, ))
    # end def _get_elem

    def __repr__ (self) :
        result = ["%s\n    > %s" % (str (self), sorted (self.jc.iteritems ()))]
        result.extend ("  %r" % c for c in self.children)
        return "\n".join (result)
    # end def __repr__

    def __str__ (self) :
        result = [str (self.elem), self._v_repr (self.init, "init")]
        if self.init != self.edit :
            result.append (self._v_repr (self.edit, "edit"))
        if self.sid is not None :
            result.append ("sid = %s" % (self.sid, ))
        result.append ("changes = %s" % (self.changes, ))
        if self.role_id is not None :
            result.append ("role_id = %s" % (self.role_id))
        return ", ".join (result)
    # end def __str__

# end class Value

if __name__ != "__main__" :
    GTW.AFS._Export ("Value")
### __END__ GTW.AFS.Value
