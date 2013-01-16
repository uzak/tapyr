# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.Attr.Kind
#
# Purpose
#    Provide descriptor classes for various attribute kinds of MOM
#
# Revision Dates
#    24-Sep-2009 (CT) Creation (factored from TOM.Attr.Kind)
#    28-Sep-2009 (CT) Creation continued
#    29-Sep-2009 (CT) Creation continued..
#     6-Oct-2009 (CT) Creation continued...: `Primary`: method redefinitions
#     7-Oct-2009 (CT) Creation continued....: `set_cooked` folded into `__set__`
#     9-Oct-2009 (CT) `_symbolic_default` and `raw_default` added
#     9-Oct-2009 (CT) `Primary.__set__` changed to raise unconditionally
#     9-Oct-2009 (CT) `Sticky_Mixin` changed to use `reset` instead of
#                     homegrown code
#    12-Oct-2009 (CT) `is_primary` and `is_settable` added
#    19-Oct-2009 (CT) `changed = 42` added to various `set`-specific methods
#                     to avoid change checks during `reset`
#    20-Oct-2009 (MH) `s/TOM/MOM/g`
#    21-Oct-2009 (CT) `Class_Uses_Default_Mixin` removed
#    22-Oct-2009 (CT) Use `M_Attr_Kind` as meta
#    22-Oct-2009 (CT) s/default/raw_default/ where necessary
#    22-Oct-2009 (CT) `_Raw_Value_Mixin_` factored
#    28-Oct-2009 (CT) I18N
#    29-Oct-2009 (CT) `rank` added
#     3-Nov-2009 (CT) `Link_Role.get_role` added
#    19-Nov-2009 (CT) `Link_Role.sort_key` added
#    20-Nov-2009 (CT) Documentation added
#    20-Nov-2009 (CT) `__all__` computed explicitly
#    23-Nov-2009 (CT) `__cmp__` and `__hash__` removed (breaks hashing of
#                     Link_Role attributes)
#    26-Nov-2009 (CT) Use `except ... as ...` (3-compatibility)
#    26-Nov-2009 (CT) `_Object_Reference_Mixin_` and `Object_Reference_Mixin`
#                     added
#    28-Nov-2009 (CT) `_Object_Reference_Mixin_._update_raw` removed
#    16-Dec-2009 (CT) `record_changes` set to False for all kinds but `_User_`
#    16-Dec-2009 (CT) Defaults for `electric`, `record_changes`, and
#                     `save_to_db` moved to `Kind`
#    17-Dec-2009 (CT) Don't `record_changes` for electric objects
#    18-Dec-2009 (CT) Use `unicode` instead of `str`
#    21-Dec-2009 (CT) `get_pickle_cargo` and `set_pickle_cargo` (and
#                     `_EPK_Mixin_`) added
#    29-Dec-2009 (CT) `get_raw` and `get_value` changed to allow `None` for
#                     `obj`
#    30-Dec-2009 (CT) `_EPK_Mixin_._set_cooked_inner` to guard for differing
#                     `home_scope`
#    30-Dec-2009 (CT) `__set__` changed to really record changes
#     5-Jan-2010 (CT) `_checkers` added to `Kind` and `Primary`
#    18-Jan-2010 (CT) `Cached_Role_Set` added
#    21-Jan-2010 (CT) `sort_key` moved from `Link_Role` to `_EPK_Mixin_`
#    21-Jan-2010 (CT) `_Sticky_Mixin_` factored (and calls to `reset` replaced)
#    21-Jan-2010 (CT) `_Primary_` factored and `Primary_Optional` added
#    21-Jan-2010 (CT) `as_arg_ckd` and `as_arg_raw` added to `Primary` and
#                     `Primary_Optional`
#    31-Jan-2010 (CT) Properties `default` and `raw_default` added and used
#                     to handle `computed_default`
#    31-Jan-2010 (CT) `Mandatory_Mixin` factored
#     2-Feb-2010 (CT) Support for `Type.Pickler` added
#     2-Feb-2010 (CT) `dependent_attrs` and `_Auto_Update_Mixin_` added
#     4-Feb-2010 (CT) Argument `e_type` added to `_checkers`
#     4-Feb-2010 (CT) `_record_change` factored
#     4-Feb-2010 (CT) `_Composite_Mixin_` and `_Nested_Mixin_` added
#     5-Feb-2010 (CT) `_Composite_Mixin_` and `_Nested_Mixin_` continued
#     8-Feb-2010 (CT) `_Auto_Update_Mixin_.update` changed to pass
#                     `changed = True` to `_set_cooked`
#     8-Feb-2010 (CT) `_Composite_Mixin_._set_cooked_value` changed to set
#                     `home_scope`, if necessary
#     8-Feb-2010 (CT) `_Computed_Mixin_` factored
#     8-Feb-2010 (CT) `Query` added
#     9-Feb-2010 (CT) `get_hash` added
#     9-Feb-2010 (CT) `_Composite_Mixin_._set_cooked_value` changed to set
#                     `is_primary`
#    10-Feb-2010 (CT) `_Composite_Mixin_.reset` and `._check_sanity` added to
#                     automatically create attribute value and disallow
#                     definition of `default` (in all guises)
#    12-Feb-2010 (CT) `Auto_Cached.get_value` changed to pass
#                     `changed = True` to `_set_cooked`
#    15-Feb-2010 (CT) `_Composite_Mixin_.set_pickle_cargo` changed to use
#                     `from_pickle_cargo` (doh)
#    16-Feb-2010 (MG) `Kind.get_pickle_cargo` and `Kind.set_pickle_cargo`
#                     fixed
#    25-Feb-2010 (CT) `Mandatory` added
#    25-Feb-2010 (CT) `_k_rank` added to `Mandatory`, `Required`, and `Optional`
#    28-Feb-2010 (CT) `_Computed_Mixin_.get_value` changed to also compute
#                     for values of `""`
#     1-Mar-2010 (CT) Record electric changes, too
#     3-Mar-2010 (CT) `_checkers` changed to pass `self` to `attr._checkers`
#    11-Mar-2010 (CT) `epk_def_set` added
#    12-Mar-2010 (CT) Interface of `attr.Pickler` changed
#    15-Mar-2010 (CT) Interface of `attr.Pickler` changed again (`attr_type`)
#    16-Mar-2010 (CT) `_Pickle_Mixin_` added
#    19-Mar-2010 (CT) `_EPK_Mixin_.get_pickle_cargo` and `.set_pickle_cargo`
#                     changed to use `ref.pid` as pickle cargo
#    19-Apr-2010 (CT) `_d_rank` added (based on sequence of definition)
#    20-Apr-2010 (CT) `Computed_Set_Mixin` added
#    22-Apr-2010 (CT) `Link_Role._set_cooked_value` redefined to reset
#                     `auto_cache`, if any, before chaining up
#    22-Apr-2010 (CT) `_Composite_Mixin_._set_cooked_value` changed to call
#                     `reset` if `value is None`
#    28-Apr-2010 (CT) `_Composite_Collection_Mixin_` added
#    18-Jun-2010 (CT) `get_raw` changed to return `u""` instead of `""`
#    22-Jun-2010 (CT) `is_mandatory` added
#    24-Jun-2010 (CT) `db_sig` added
#    28-Jun-2010 (CT) Missing import for `TFL.Meta.Once_Property` added
#    29-Jun-2010 (CT) s/from_pickle_cargo/from_attr_pickle_cargo/
#                     s/as_pickle_cargo/as_attr_pickle_cargo/
#     1-Jul-2010 (MG) `get_pickle_cargo` and `set_pickle_cargo` changed to
#                     always return a tuple/accept a tupple
#     1-Jul-2010 (MG) `_Pickle_Mixin_` removed
#    18-Aug-2010 (CT) `_Composite_Collection_Mixin_`: added `reset` and
#                     `_set_cooked_value`
#    18-Aug-2010 (CT) `_check_sanity_default` factored and redefined for
#                     `_A_Composite_Collection_`
#    18-Aug-2010 (CT) `_update_owner` factored and used in
#                     `_Composite_Collection_Mixin_._set_cooked_value`
#    19-Aug-2010 (CT) `get_substance` and `void_values` factored and added to
#                     `_Composite_Mixin_`
#     2-Sep-2010 (CT) Signatures of `Pickler.as_cargo` and `.from_cargo` changed
#     2-Sep-2010 (CT) `from_pickle_cargo` factored
#     4-Sep-2010 (CT) `_Co_Base_` and `_Collection_Base_` factored,
#                     `_Typed_Collection_Mixin_` added
#     4-Sep-2010 (CT) `_Computed_Mixin_._get_value` changed to use `void_values`
#     6-Sep-2010 (CT) `_Computed_Collection_Mixin_` removed
#     7-Sep-2010 (CT) `_Typed_Collection_Mixin_.__init__` changed to replace
#                     `attr.R_Type` from `M_Coll.Table` if `record_changes`
#    22-Sep-2010 (CT) `void_raw_values` factored
#    28-Sep-2010 (CT) `get_raw_epk` added
#    14-Oct-2010 (CT) Last vestiges of `_symbolic_default` removed
#    14-Oct-2010 (CT) `_set_cooked_value_inner` factored
#    14-Oct-2010 (CT) `Init_Only_Mixin` added
#    22-Nov-2010 (CT) `_Raw_Value_Mixin_` changed to use `get_pickle_cargo`
#                     and `from_pickle_cargo` of `__super` to support
#                     `attr.Pickler`, if any
#     9-Dec-2010 (CT) `_Auto_Update_Lazy_Mixin_` added
#     8-Feb-2011 (CT) s/Required/Necessary/, s/Mandatory/Required/
#    29-Mar-2011 (CT) `is_changeable` and `Just_Once_Mixin` added
#    22-Sep-2011 (CT) s/Object_Reference_Mixin/Id_Entity_Reference_Mixin/
#    22-Sep-2011 (CT) s/Class/P_Type/ for _A_Id_Entity_ attributes
#    22-Sep-2011 (CT) s/C_Type/P_Type/ for _A_Composite_ attributes
#     8-Nov-2011 (CT) Add `Id_Entity_Reference_Mixin._check_sanity` for `P_Type`
#     8-Nov-2011 (CT) Use `Error.Required_Empty` for `_Required_Mixin_` check
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    19-Jan-2012 (CT) Change `Id_Entity_Reference_Mixin._set_cooked_value` to
#                     consider `obj._home_scope`, append to `obj._init_pending`
#     6-Mar-2012 (CT) Add sanity check for `Syntax_Re_Mixin`
#    24-Mar-2012 (CT) Use `acr_map` to get cacher for `Link_Role`
#    11-Apr-2012 (CT) Change `Id_Entity_Reference_Mixin._set_cooked_value` to
#                     always append to `obj._init_pending`
#    15-Apr-2012 (CT) Adapted to changes of `MOM.Error`
#    19-Apr-2012 (CT) Use translated `.ui_name` instead of `.type_name` for
#                     exceptions
#     4-May-2012 (CT) Add I18N marker `_` to `kind = <kind>` statements
#    13-Jun-2012 (CT) Add call of `_finish__init__` to
#                     `_Composite_Mixin_.from_pickle_cargo`
#     4-Aug-2012 (CT) Change `Id_Entity_Reference_Mixin._set_cooked_value` to
#                     only append to `obj._init_pending` if not `init_finished`
#                     (I don't know what I'd smoked on 11-Apr-2012 :-( )
#     5-Aug-2012 (CT) Add/use `get_raw_pid`
#     8-Aug-2012 (CT) Use `logging` instead of `print`
#    20-Aug-2012 (RS) import `logging`
#    21-Aug-2012 (RS) Expand logged args in place, fix format string arg count
#     8-Sep-2012 (CT) Consider `init_finished` in `Link_Role._set_cooked_value`
#    12-Sep-2012 (CT) Add `__init__` argument `e_type`
#    11-Oct-2012 (CT) Use `sig_rank` instead of home-grown code
#    14-Dec-2012 (CT) Add guard to `Query._get_computed`
#    11-Jan-2013 (CT) Add `Primary_AIS`; factor `_Primary_D_`,
#                     derive `_Primary_` from `Kind`, not `_User_`
#    16-Jan-2013 (CT) Add `Primary_AIS.get_substance`, `.has_substance`
#    16-Jan-2013 (CT) Add `Primary_AIS.__set__`
#    ��revision-date�����
#--

from   __future__            import unicode_literals

from   _TFL                  import TFL
from   _MOM                  import MOM

import _TFL._Meta.Once_Property
import _TFL._Meta.Property
import _TFL.Functor

import _MOM._Attr
import _MOM._Meta.M_Attr_Kind
import _MOM._Prop.Kind

from   _TFL.I18N             import _, _T, _Tn

import logging
import pickle

class Kind (MOM.Prop.Kind) :
    """Root class of attribute kinds to be used as properties for essential
       attributes of the MOM meta object model.
    """

    __metaclass__         = MOM.Meta.M_Attr_Kind

    attr                  = None
    db_sig_version        = 0
    electric              = True
    is_changeable         = True
    is_primary            = False
    is_required           = False
    is_settable           = True
    needs_raw_value       = False
    prop                  = TFL.Meta.Alias_Property ("attr")
    record_changes        = False
    save_to_db            = False
    sync                  = None
    Table                 = dict ()
    void_values           = property (lambda s : (None, ""))
    void_raw_values       = property (lambda s : ("", s.attr.raw_default))

    _k_rank               = 0

    def __init__ (self, Attr_Type, e_type) :
        attr = Attr_Type      (self, e_type)
        self.__super.__init__ (attr, e_type)
        self._check_sanity    (attr, e_type)
        self.dependent_attrs = set ()
        self.rank            = attr.sig_rank
        self.record_changes  = attr.record_changes and self.record_changes
    # end def __init__

    def __delete__ (self, obj) :
        self.reset (obj)
        if self.dependent_attrs :
            man = obj._attr_man
            man.updates_pending = list (self.dependent_attrs)
            man.do_updates_pending (obj)
    # end def __delete__

    def __get__ (self, obj, cls) :
        if obj is None :
            return self
        return self.get_value (obj)
    # end def __get__

    def __set__ (self, obj, value) :
        old_value = self.get_value   (obj)
        old_raw   = self.get_raw_pid (obj)
        changed   = old_value != value
        self.attr.check_invariant (obj, value)
        self._set_cooked          (obj, value, changed)
        if changed :
            if self.dependent_attrs :
                man = obj._attr_man
                man.updates_pending = list (self.dependent_attrs)
                man.do_updates_pending (obj)
            if self.record_changes :
                self._record_change (obj, value, self.name, old_raw)
    # end def __set__

    @TFL.Meta.Once_Property
    def db_sig (self) :
        return \
            ( self.db_sig_version
            , self.is_required
            , self.is_primary
            , self.needs_raw_value
            , self.attr.db_sig
            )
    # end def db_sig

    @property
    def default (self) :
        attr = self.attr
        if TFL.callable (attr.computed_default) :
            result = attr.computed_default ()
        else :
            result = attr.default
        return result
    # end def default

    def from_pickle_cargo (self, scope, cargo) :
        Pickler = self.attr.Pickler
        if Pickler :
            return Pickler.from_cargo (scope, self, self.attr, cargo [0])
        return cargo [0]
    # end def from_pickle_cargo

    def get_hash (self, obj, value = None) :
        return value if (value is not None) else self.get_value (obj)
    # end def get_hash

    def get_pickle_cargo (self, obj) :
        Pickler = self.attr.Pickler
        value   = self.get_value (obj)
        if Pickler :
            return (Pickler.as_cargo (self, self.attr, value), )
        else :
            return (value, )
    # end def get_pickle_cargo

    def get_raw (self, obj) :
        if obj is not None :
            val = self.get_value (obj)
            if val is not None :
                result = self.attr.as_string (val) or u""
            else :
                result = u""
        else :
            result = self.raw_default
        return result
    # end def get_raw

    def get_raw_epk (self, obj) :
        return self.get_raw (obj)
    # end def get_raw_epk

    def get_raw_pid (self, obj) :
        return self.get_raw (obj)
    # end def get_raw_pid

    def get_value (self, obj) :
        if obj is not None :
            return getattr (obj, self.attr.ckd_name, None)
        else :
            return self.default
    # end def get_value

    def inc_changes (self, man, obj, value) :
        ### don't redefine this (redefine `_inc_changes` instead)
        ### (this allows applications to extend `inc_changes` without having
        ### to know all classes redefining `_inc_changes`) !!!
        return self._inc_changes (man, obj, value)
    # end def inc_changes

    @property
    def raw_default (self) :
        attr = self.attr
        if TFL.callable (attr.computed_default) :
            result = attr.as_string (attr.computed_default ())
        else :
            result = attr.raw_default
        return result
    # end def default

    def reset (self, obj) :
        attr = self.attr
        if attr.raw_default and attr.default is None :
            attr.default = attr.from_string \
                (attr.raw_default, obj, obj.globals ())
        return self._set_raw \
            (obj, attr.raw_default, attr.default, changed = True)
    # end def reset

    def set_pickle_cargo (self, obj, cargo) :
        value = self.from_pickle_cargo (obj.home_scope, cargo)
        if value is not None :
            self._set_cooked_value (obj, value, changed = True)
    # end def set_pickle_cargo

    def set_raw (self, obj, raw_value, glob_dict = None, dont_raise = False, changed = 42) :
        if glob_dict is None :
            glob_dict = obj.globals ()
        value = None
        if raw_value :
            try :
                value = self.attr.from_string (raw_value, obj, glob_dict)
                self.attr.check_invariant     (obj, value)
            except StandardError as exc :
                if dont_raise :
                    if __debug__ :
                        logging.exception \
                            ("set_raw %s %r -> %r" % (obj, raw_value, value))
                else :
                    raise
        return self._set_raw (obj, raw_value, value, changed)
    # end def set_raw

    def sync_cooked (self, obj, raw_value) :
        if __debug__ :
            print _T \
                ( "Trying to sync pending attribute %s of %s to `%s`"
                ) % (self.name, obj.name, raw_value)
        self.set_raw (obj, raw_value)
    # end def sync_cooked

    def to_save (self, obj) :
        return False
    # end def to_save

    def _checkers (self, e_type) :
        for c in self.attr._checkers (e_type, self) :
            yield c
    # end def _checkers

    def _check_sanity (self, attr_type, e_type) :
        if __debug__ :
            self._check_sanity_default (attr_type, e_type)
            if isinstance (attr_type, attr_type.Syntax_Re_Mixin) :
                if attr_type._syntax_re is None :
                    raise ValueError \
                        ( "`%s` needs a definition for `_syntax_re`"
                        % (attr_type, )
                        )
            elif isinstance (attr_type, MOM.Attr.A_AIS_Value) :
                if not isinstance (self, Primary_AIS) :
                    raise TypeError \
                        ( "`%s` needs to be kind Primary_AIS, but is %s"
                        % (attr_type, self.__class__)
                        )
                if attr_type.default is not None :
                    raise TypeError \
                        ( "`%s` needs default `None`, but has default `%s`"
                        % (attr_type, attr_type.default)
                        )
                if not e_type.relevant_root :
                    raise TypeError \
                        ( "Attribute `%s` cannot be defined for non-relevant "
                          "E-Type s"
                        % (attr_type, e_type)
                        )
    # end def _check_sanity

    def _check_sanity_default (self, attr_type, e_type) :
        default = getattr (attr_type, "raw_default", None)
        if (   default is not None
           and not isinstance (default, basestring)
           ) :
            d = attr_type.as_string (default)
            if d == "" and default is not None :
                d = u"%s" % default
            raise ValueError \
                ( u""">>> %s.%s: got `%s` instead of "%s" as `raw_default`"""
                % (attr_type, self.name, default, d)
                )
    # end def _check_sanity_default

    def _get_computed (self, obj) :
        attr     = self.attr
        computed = attr.computed
        if TFL.callable (computed) :
            val = computed (obj)
            if val is not None :
                return attr.cooked (val)
    # end def _get_computed

    def _inc_changes (self, man, obj, value) :
        man.inc_changes ()
    # end def _inc_changes

    def _record_change (self, obj, value, name, old_raw) :
        obj.home_scope.record_change \
            (MOM.SCM.Change.Attr, obj, {name : old_raw})
    # end def _record_change

    def _set_cooked (self, obj, value, changed = 42) :
        return self._set_cooked_inner (obj, value, changed)
    # end def _set_cooked

    def _set_cooked_inner (self, obj, value, changed = 42) :
        if value is not None :
            try :
                value = self.attr.cooked (value)
            except StandardError as exc :
                if __debug__ :
                    logging.exception \
                        ( "%s: %s.%s, value `%s` [%r]"
                        % (self.attr, obj.type_base_name, self.name, value, obj)
                        )
                raise
        return self._set_cooked_value (obj, value, changed)
    # end def _set_cooked_inner

    def _set_cooked_value (self, obj, value, changed = 42) :
        if changed == 42 :
            ### if the caller didn't pass a (boolean) value, evaluate it here
            changed = self.get_value (obj) != value
        if changed :
            attr_man = obj._attr_man
            self._set_cooked_value_inner (obj, value)
            self.inc_changes (attr_man, obj, value)
            if self.dependent_attrs :
                attr_man.updates_pending.extend (self.dependent_attrs)
            return True
    # end def _set_cooked_value

    def _set_cooked_value_inner (self, obj, value) :
        setattr (obj, self.attr.ckd_name, value)
    # end def _set_cooked_value_inner

    def _set_raw (self, obj, raw_value, value, changed = 42) :
        return self._set_cooked_inner (obj, value, changed)
    # end def _set_raw

    def _set_raw_inner (self, obj, raw_value, value, changed = 42) :
        pass
    # end def _set_raw_inner

    def __repr__ (self) :
        return "%s `%s`" % (self.attr.typ, self.name)
    # end def __repr__

# end class Kind

class _EPK_Mixin_ (Kind) :
    """Mixin for attributes referring to entities with `epk`."""

    @TFL.Meta.Once_Property
    def db_sig (self) :
        return self.__super.db_sig + (self.attr.P_Type.type_name, )
    # end def db_sig

    def get_raw_epk (self, obj) :
        ref = self.get_value (obj)
        if ref is not None :
            return ref.epk_raw
        return u""
    # end def get_raw_epk

    def get_raw_pid (self, obj) :
        ref = self.get_value (obj)
        if ref is not None :
            return ref.pid
        return u""
    # end def get_raw_pid

    def from_pickle_cargo (self, scope, cargo) :
        if cargo and cargo [0] :
            ETM = scope [self.attr.P_Type.type_name]
            return ETM.pid_query (cargo [0])
    # end def from_pickle_cargo

    def get_hash (self, obj, value = None) :
        ref = value if (value is not None) else self.get_value (obj)
        if ref is not None :
            return ref.pid
    # end def get_hash

    def get_pickle_cargo (self, obj) :
        ref = self.get_value (obj)
        if ref is not None :
            return (ref.pid, )
        return (None, )
    # end def get_pickle_cargo

    def sort_key (self, obj) :
        v = self.get_value (obj)
        return v.__class__.sort_key (v)
    # end def sort_key

    def sort_key_pm (self, obj) :
        v = self.get_value (obj)
        return v.__class__.sort_key_pm () (v)
    # end def sort_key_pm

    def _set_cooked_inner (self, obj, value, changed = 42) :
        scope = obj.home_scope
        if value is not None and scope != value.home_scope :
            etm = scope [value.type_name]
            val = etm.instance (* value.epk_raw_pid, raw = True)
            if val is None :
                raise MOM.Error.Link_Scope_Mix \
                    (_T (value.ui_name), value, value.home_scope, obj, scope)
            else :
                value = val
        return self._set_cooked_value (obj, value, changed)
    # end def _set_cooked_inner

# end class _EPK_Mixin_

class _Required_Mixin_ (Kind) :
    """Mixin for enforcing that an attribute always has a value"""

    is_required          = True

    def _checkers (self, e_type) :
        name = self.name
        yield MOM.Pred.Attribute_Check \
            ( name       = "%s_not_empty" % (name, )
            , attr       = name
            , assertion  = "value is not None and value != ''"
            , attr_none  = (name, )
            , kind       = MOM.Pred.Object
            , Error_Type = MOM.Error.Required_Empty
            )
        for c in self.__super._checkers (e_type) :
            yield c
    # end def _checkers

# end class _Required_Mixin_

class _Auto_Update_Mixin_ (Kind) :
    """Mixin to auto-update an attribute after changes of any other attribute
       it depends on, as specified by `auto_up_depends`.
    """

    def update (self, obj) :
        self._set_cooked (obj, self._get_computed (obj), True)
    # end def update

    def _check_sanity (self, attr_type, e_type) :
        self.__super._check_sanity (attr_type, e_type)
        if __debug__ :
            if not attr_type.auto_up_depends :
                raise TypeError \
                    ( "%s is defined as `Auto_Update_Mixin` but has no "
                      "`auto_up_depends` specified"
                    % (attr_type, )
                    )
    # end def _check_sanity

# end class _Auto_Update_Mixin_

class _Auto_Update_Lazy_Mixin_ (_Auto_Update_Mixin_) :
    """Mixin to lazily auto-update an attribute after changes of any other
       attribute it depends on, as specified by `auto_up_depends`.
    """

    def update (self, obj) :
        ### reset value so that `compute` is triggered at next access
        ### (but don't call `reset` to avoid overhead, e.g. `inc_changes`)
        self._set_cooked_value_inner (obj, self.attr.default)
    # end def update

# end class _Auto_Update_Lazy_Mixin_

class _Co_Base_ (Kind) :
    """Base for collection and composite mixin classes."""

    def _set_cooked_value (self, obj, value, changed = 42) :
        if value is None :
            ### Need an empty collection/composite at all times
            return self.reset (obj)
        else :
            if not self.electric :
                value = self._update_owner (obj, value)
            return self.__super._set_cooked_value (obj, value, changed)
    # end def _set_cooked_value

    def _update_owner (self, obj, value) :
        if value.owner is not None and value.owner is not obj :
            value = value.copy ()
        value.attr_name    = self.name
        value.owner        = obj
        value.home_scope   = obj.home_scope
        return value
    # end def _update_owner

# end class _Co_Base_

class _Composite_Mixin_ (_Co_Base_) :
    """Mixin for composite attributes."""

    get_substance   = TFL.Meta.Alias_Property ("get_raw")
    void_values     = property (lambda s : s.void_raw_values)

    def from_pickle_cargo (self, scope, cargo) :
        if cargo and cargo [0] :
            result = self.attr.P_Type.from_attr_pickle_cargo (scope, cargo [0])
            result._finish__init__ ()
            return result
    # end def from_pickle_cargo

    def get_hash (self, obj, value = None) :
        if value is None :
            value = self.get_value (obj)
        if value is not None :
            if value.hash_sig :
                return value.hash_key
            else :
                return id (value)
    # end def get_hash

    def get_pickle_cargo (self, obj) :
        value = self.get_value (obj)
        if value is not None :
            return (value.as_attr_pickle_cargo (), )
        return (None, )
    # end def get_pickle_cargo

    def reset (self, obj) :
        ### Need an empty composite at all times
        scope = obj.home_scope
        etm   = scope [self.attr.P_Type.type_name]
        return self._set_cooked_value (obj, etm (), changed = True)
    # end def reset

    def _check_sanity (self, attr_type, e_type) :
        if __debug__ :
            if not attr_type.P_Type :
                raise TypeError \
                    ("%s needs to define `P_Type`" % attr_type)
            for name in ("computed_default", "default", "raw_default") :
                d = getattr (attr_type, name)
                if d :
                    raise TypeError \
                        ( "Attribute `%s` of kind %s cannot have %s %r"
                        % (attr_type, self.kind, name, d)
                        )
        self.__super._check_sanity (attr_type, e_type)
    # end def _check_sanity

    def _update_owner (self, obj, value) :
        self.__super._update_owner (obj, value)
        if value.owner is not obj :
            value._attr_man.inc_changes ()
        return value
    # end def _update_owner

# end class _Composite_Mixin_

class _Typed_Collection_Mixin_ (_Co_Base_) :
    """Mixin for typed collection attributes."""

    void_values = property \
        (lambda s : ("", s.attr.raw_default, s.attr.R_Type ()))

    def __init__ (self, Attr_Type, e_type) :
        self.__super.__init__ (Attr_Type, e_type)
        attr = self.attr
        if self.record_changes :
            PT = MOM.Attr.M_Coll.Table.get (attr.R_Type)
            if PT is not None :
                attr.R_Type = PT.New (attr_name = attr.name)
            elif attr.R_Type is not tuple :
                if __debug__ :
                    logging.exception \
                        ( "%s: R_Type %r doesn't have a correspondence in "
                          "MOM.Attr.Coll; is it immutable?"
                        % (attr, attr.R_Type)
                        )
    # end def __init__

    def reset (self, obj) :
        ### Need an empty collection at all times
        return self._set_cooked_value (obj, self.attr.R_Type (), changed = True)
    # end def reset

    def _check_sanity (self, attr_type, e_type) :
        if __debug__ :
            if isinstance (self, _Primary_) :
                raise TypeError \
                    ("%s cannot be of primary kind %" % (attr_type, self.kind))
            C_Type = attr_type.C_Type
            if not C_Type :
                raise TypeError ("%s needs to define `C_Type`" % attr_type)
        self.__super._check_sanity (attr_type, e_type)
    # end def _check_sanity

    def _check_sanity_default (self, attr_type, e_type) :
        default = getattr (attr_type, "raw_default", None)
        if default is not None and default not in ([], ()) :
            self.__super._check_sanity_default (attr_type, e_type)
    # end def _check_sanity_default

# end class _Typed_Collection_Mixin_

class _Computed_Mixin_ (Kind) :
    """Mixin to compute attribute value."""

    def get_value (self, obj) :
        result = self.__super.get_value (obj)
        if obj is not None and (result is None or result in self.void_values) :
            result = self._get_computed (obj)
        return result
    # end def get_value

    def _check_sanity (self, attr_type, e_type) :
        self.__super._check_sanity (attr_type, e_type)
        default = self.raw_default
        if default :
            kind = self.kind
            if kind != "computed" :
                kind += "/Computed"
            raise TypeError \
                ( "%s is %s but has default %r "
                  "(i.e., `computed` will never be called)\n    %s"
                % (attr_type, kind, default, self.__class__.mro ())
                )
    # end def _check_sanity

# end class _Computed_Mixin_

class _Nested_Mixin_ (Kind) :
    """Mixin for attributes nested inside composite attributes."""

    def _inc_changes (self, man, obj, value) :
        self.__super._inc_changes (man, obj, value)
        if obj.owner is not None :
            obj.owner._attr_man.inc_changes ()
    # end def _inc_changes

    def _record_change (self, obj, value, name, old_raw) :
        if obj.owner is not None :
            obj.home_scope.record_change \
                (MOM.SCM.Change.Attr_Composite, obj, {name : old_raw})
    # end def _record_change

# end class _Nested_Mixin_

class _Raw_Value_Mixin_ (Kind) :
    """Mixin for keeping raw values of user-specified attributes."""

    get_substance   = TFL.Meta.Alias_Property ("get_raw")
    needs_raw_value = True
    void_values     = property (lambda s : s.void_raw_values)

    def get_pickle_cargo (self, obj) :
        return self.__super.get_pickle_cargo (obj) [0], self.get_raw (obj)
    # end def get_pickle_cargo

    def get_raw (self, obj) :
        if obj is not None :
            result = getattr (obj, self.attr.raw_name, u"")
        else :
            result = self.raw_default
        return result
    # end def get_raw

    def get_value (self, obj) :
        if obj is not None and obj._attr_man.needs_sync.get (self.name) :
            self._sync (obj)
        return self.__super.get_value (obj)
    # end def get_value

    def set_pickle_cargo (self, obj, cargo) :
        ckd = self.from_pickle_cargo (obj.home_scope, cargo)
        if len (cargo) > 1 :
            raw = cargo [1]
            self._set_cooked_value (obj,      ckd, changed = True)
            self._set_raw_inner    (obj, raw, ckd, changed = True)
        else :
            self._set_cooked       (obj,      ckd, changed = True)
    # end def set_pickle_cargo

    def _set_cooked (self, obj, value, changed = 42) :
        self._set_cooked_inner (obj, value, changed)
        self._set_raw_inner (obj, self.attr.as_string (value), value, changed)
    # end def _set_cooked

    def _set_raw (self, obj, raw_value, value, changed = 42) :
        if changed == 42 :
            ### if the caller didn't pass a (boolean) value, evaluate it here
            changed = raw_value != self.get_raw (obj)
        if changed :
            self.inc_changes  (obj._attr_man, obj, value)
        self.__super._set_raw (obj, raw_value, value, changed)
        self._set_raw_inner   (obj, raw_value, value, changed)
    # end def _set_raw

    def _set_raw_inner (self, obj, raw_value, value, changed = 42) :
        setattr (obj, self.attr.raw_name, raw_value)
    # end def _set_raw_inner

    def _sync (self, obj) :
        raw_value = self.get_raw_pid (obj)
        value     = None
        if raw_value :
            try :
                value = self.attr.from_string (raw_value, obj, obj.globals ())
            except StandardError as exc :
                if __debug__ :
                    logging.exception \
                        ("%s._sync: %s -> %r" % (self, obj, raw_value))
        self._set_cooked_inner (obj, value)
        obj._attr_man.needs_sync [self.name] = False
    # end def _sync

# end class _Raw_Value_Mixin_

class _Sticky_Mixin_ (Kind) :

    def _set_cooked (self, obj, value, changed = 42) :
        if value is None :
            value = self.default
        self.__super._set_cooked (obj, value, changed)
    # end def _set_cooked

    def _set_raw (self, obj, raw_value, value, changed = 42) :
        if raw_value in ("", None) :
            raw_value = self.raw_default
            value     = self.default
        self.__super._set_raw (obj, raw_value, value, changed)
    # end def _set_raw

# end class _Sticky_Mixin_

class _DB_Attr_ (Kind) :
    """Attributes stored in DB."""

    record_changes = True
    save_to_db     = True

    def to_save (self, obj) :
        raw_val = self.get_raw (obj)
        result  = bool (raw_val)
        if result and not self.store_default :
            result = raw_val != self.attr.raw_default
        return result
    # end def to_save

# end class _DB_Attr_

class _User_ (_DB_Attr_, Kind) :
    """Attributes set by user."""

    electric              = False
    get_substance         = TFL.Meta.Alias_Property ("get_value")
    void_values           = property (lambda s : (None, s.attr.default))

    def has_substance (self, obj) :
        return self.get_substance (obj) not in self.void_values
    # end def has_substance

# end class _User_

class _System_ (Kind) :
    """Attributes set by system."""

# end class _System_

class _DB_System_ (_DB_Attr_, _System_) :
    pass
# end class _DB_System_

class _Volatile_ (Kind) :
    """Attributes not stored in DB."""

# end class _Volatile_

class _Cached_ (_Volatile_, _System_) :

    is_settable = False
    kind        = _ ("cached")

    def _inc_changes (self, man, obj, value) :
        pass
    # end def _inc_changes

# end class _Cached_

class _Primary_ (Kind) :

    is_primary  = True
    kind        = _ ("primary")

    def __set__ (self, obj, value) :
        raise AttributeError \
            ( "\n".join
                ( ( _T ( "Primary attribute `%s.%s` cannot be assigned.")
                  , _T ("Use `set` or `set_raw` to change it.")
                  )
                )
            % (_T (obj.ui_name), self.name)
            )
    # end def __set__

    def __delete__ (self, obj, value) :
        raise AttributeError \
            ( _T ("Primary attribute `%s.%s` cannot be deleted")
            % (_T (obj.ui_name), self.name)
            )
    # end def __delete__

    def to_save (self, obj) :
        return True
    # end def to_save

# end class _Primary_

class _Primary_D_ (_Primary_) :

    @classmethod
    def as_arg_ckd (cls, attr) :
        return "%s = %r" % (attr.name, attr.default)
    # end def as_arg_ckd

    @classmethod
    def as_arg_raw (cls, attr) :
        return "%s = %r" % (attr.name, attr.raw_default)
    # end def as_arg_raw

    @classmethod
    def epk_def_set (cls, code) :
        return code
    # end def epk_def_set

# end class _Primary_D_

class Primary (_Required_Mixin_, _Primary_, _User_) :
    """Primary attribute: must be defined at all times, used as part of the
       `essential primary key`.
    """

    _k_rank     = -20

    @classmethod
    def as_arg_ckd (cls, attr) :
        return attr.name
    # end def as_arg_ckd

    as_arg_raw = as_arg_ckd

    @classmethod
    def epk_def_set (cls, code) :
        pass
    # end def epk_def_set

# end class Primary

class Primary_AIS (_Primary_D_, _DB_System_) :
    """Primary auto-incremented-sequence attribute:
       cannot be passed to constructor,
       used as part of the `essential primary key`.
    """

    _k_rank     = -5

    get_substance         = TFL.Meta.Alias_Property ("get_value")
    void_values           = property (lambda s : ())

    def has_substance (self, obj) :
        return True
    # end def has_substance

    def __set__ (self, obj, value) :
        self._set_cooked_value_inner (obj, value)
    # end def __set__

# end class Primary_AIS

class Primary_Optional (_Sticky_Mixin_, _Primary_D_, _User_) :
    """Primary optional attribute: has a default value, used as part
       of the `essential primary key`.
    """

    _k_rank     = -10

# end class Primary_Optional

class Link_Role (_EPK_Mixin_, Primary) :
    """Link-role attribute must be defined at all times, used for (essential)
       primary key.
    """

    get_role               = TFL.Meta.Alias_Property ("get_value")

    def _set_cooked_value (self, obj, value, changed = 42) :
        if obj.init_finished :
            ac = obj.__class__.acr_map.get (self.name)
            if ac :
                old_value = self.get_value (obj)
                if old_value is not None :
                    ### remove old value from `auto_cache`
                    ac (obj, no_value = True)
        return self.__super._set_cooked_value (obj, value, changed = changed)
    # end def _set_cooked_value

# end class Link_Role

class Required (_Required_Mixin_, _User_) :
    """Required attribute: must immediately be defined by the tool user."""

    kind        = _ ("required")
    void_values = (None, "")

    _k_rank     = -5

    def to_save (self, obj) :
        return True
    # end def to_save

# end class Required

class Necessary (_User_) :
    """Necessary attribute: must eventually be defined by the tool user."""

    kind        = _ ("necessary")
    _k_rank     = -4

    def to_save (self, obj) :
        return self.has_substance (obj)
    # end def to_save

# end class Necessary

class Optional (_User_) :
    """Optional attribute: if undefined, the `default` value is used, if any."""

    kind        = _ ("optional")
    _k_rank     = -4

# end class Optional

class Internal (_DB_System_) :
    """Internal attribute: value is defined by some component of the tool."""

    kind = _ ("internal")

# end class Internal

class Const (_Cached_) :
    """Constant attribute (has static default value that cannot be changed)."""

    kind        = _ ("constant")

    def __set__ (self, obj, value) :
        raise AttributeError \
            ( _T ("Constant attribute `%s.%s` cannot be changed")
            % (_T (obj.ui_name), self.name)
            )
    # end def __set__

# end class Const

class Cached (_Cached_) :
    """Cached attribute: value is defined by some component of the tool, but
       not saved to DB.
    """

# end class Cached

class Sync_Cached (_Cached_) :
    """Cached attribute computed automatically when syncing. This kind can be
       used for attributes depending on attributes of different objects,
       as long those don't change significantly between syncing --- use
       :class:`Computed` otherwise.
    """

    def sync (self, obj) :
        self._set_cooked (obj, self._get_computed (obj))
        obj._attr_man.needs_sync [self.name] = False
    # end def sync

    def get_raw (self, obj) :
        if obj is not None and obj._attr_man.needs_sync [self.name] :
            self.sync (obj)
        return self.__super.get_raw (obj)
    # end def get_raw

    def get_value (self, obj) :
        if obj is not None and obj._attr_man.needs_sync [self.name] :
            self.sync (obj)
        return self.__super.get_value (obj)
    # end def get_value

    def reset (self, obj) :
        self.__super.reset (obj)
        obj._attr_man.needs_sync [self.name] = True
    # end def reset

# end class Sync_Cached

class Auto_Cached (_Cached_) :
    """Cached attribute that is recomputed whenever it is accessed after one
       or more of the other attributes changed since the last recomputation.

       This kind must **not** be used if the value of the attribute depends
       on other objects (use :class:`Sync_Cached` or :class:`Computed` if
       that's the case).
    """

    def get_value (self, obj) :
        if obj is not None :
            man = obj._attr_man
            if ((man.total_changes != man.update_at_changes.get (self.name, -1))
               or self.attr.ckd_name not in obj.__dict__
               ) :
                val = self._get_computed (obj)
                if val is None :
                    return
                self._set_cooked (obj, val, True)
                man.update_at_changes [self.name] = man.total_changes
        return self.__super.get_value (obj)
    # end def get_value

    def reset (self, obj) :
        obj._attr_man.update_at_changes [self.name] = -1
    # end def reset

# end class Auto_Cached

class Once_Cached (_Cached_) :
    """Cached attribute computed just once (a.k.a. computed constant).
       This kind can be used if the `constant` value that is computed depends
       on attributes of different objects, as longs as those don't change
       during the lifetime of this attribute's object.
    """

    def reset (self, obj) :
        val = self.get_value (obj)
        if val is None :
            val = self._get_computed (obj)
            self._set_cooked_inner   (obj, val, changed = True)
    # end def reset

# end class Once_Cached

class Cached_Role (_Cached_) :
    """Cached attribute automagically updated by association (max_links == 1)."""

    def reset (self, obj) :
        pass
    # end def reset

# end class Cached_Role

class Cached_Role_DFC (Cached_Role) :
    """Cached attribute normally updated by association but asking
       association for DFC_Link.
    """

    def get_value (self, obj) :
        result = self.__super.get_value (obj)
        if obj is not None and result is None :
            ### XXX
            assoc = getattr (obj.home_scope, self.attr.assoc)
            links = getattr (assoc, self.attr.name) (obj)
            if links :
                assert len (links) == 1
                result = getattr (links [0], self.attr.name)
        return result
    # end def get_value

# end class Cached_Role_DFC

class Cached_Role_Set (_Cached_) :
    """Cached attribute automagically updated by association (max_links > 1)."""

    def reset (self, obj) :
        self._set_cooked_value (obj, set (), changed = True)
    # end def reset

# end class Cached_Role

class Computed (_Cached_, _Computed_Mixin_) :
    """Computed attribute: the value is computed for each and every attribute
       access. This is quite inefficient and should only be used if
       :class:`Auto_Cached` or :class:`Sync_Cached` don't work.
    """

    kind        = _ ("computed")

    def get_value (self, obj) :
        return self._get_computed (obj)
    # end def get_value

    def reset (self, obj) :
        pass
    # end def reset

    def __set__ (self, obj, value) :
        raise AttributeError \
            ( _T ("Computed attribute `%s.%s` cannot be assigned")
            % (_T (obj.ui_name), self.name)
            )
    # end def __set__

# end class Computed

class Query (_Cached_, _Computed_Mixin_) :
    """Attribute calculated from a `query` (must be defined for the attribute
       type).
    """

    kind       = _ ("query")

    def _get_computed (self, obj) :
        attr   = self.attr
        result = attr.query (obj)
        ### `attr.query` sometimes returns a `object` instance instead of None
        if result is not None and result.__class__ is not object :
            return attr.cooked (result)
    # end def _get_computed

    def _check_sanity (self, attr_type, e_type) :
        self.__super._check_sanity (attr_type, e_type)
        if __debug__ :
            if not attr_type.auto_up_depends :
                raise TypeError \
                    ( "Attribute `%s` of kind Query needs "
                      "`auto_up_depends` specified"
                    % (attr_type, )
                    )
            query = getattr (attr_type, "query", None)
            if not TFL.callable (query) :
                raise TypeError \
                    ( "Attribute `%s` of kind Query needs to define a "
                      "`query` expression or `query_fct` method"
                    % (attr_type, )
                    )
    # end def _check_sanity

# end class Query

class Computed_Mixin (_Computed_Mixin_) :
    """Mixin to compute attribute value if empty, i.e., if no value was
       specified by the tool user.
    """

# end class Computed_Mixin

class Computed_Set_Mixin (Computed_Mixin) :
    """Mixin to compute attribute and set value if empty."""

    def get_value (self, obj) :
        attr   = self.attr
        result = self.__super.get_value (obj)
        if obj is not None and result != getattr (obj, attr.ckd_name, None) :
            self._set_cooked (obj, result, True)
        return result
    # end def get_value

# end class Computed_Set_Mixin

class Just_Once_Mixin (Kind) :
    """Mixin allowing attribute to be set to a non-default valuer just once."""

    is_changeable         = False
    _x_format             = _ \
        ( "Attribute `%s.%s` cannot be "
          "changed from `%s` to `%s`; it can be set only once!"
        )

    def _change_forbidden (self, old_value) :
        return old_value != self.default
    # end def _change_forbidden

    def _set_cooked_value_inner (self, obj, value) :
        if obj.init_finished :
            old_value = self.get_value (obj)
            if self._change_forbidden (old_value) :
                raise AttributeError \
                    ( _T (self._x_format)
                    % (_T (obj.ui_name), self.name, old_value, value)
                    )
        self.__super._set_cooked_value_inner (obj, value)
    # end def _set_cooked_value_inner

# end class Just_Once_Mixin

class Init_Only_Mixin (Just_Once_Mixin) :
    """Mixin restricting attribute changes to the object initialization."""

    _x_format             = _ \
        ( "Init-only attribute `%s.%s` cannot be "
          "changed from `%s` to `%s` after object creation"
        )

    def _change_forbidden (self, old_value) :
        return True
    # end def _change_forbidden

# end class Init_Only_Mixin

class Sticky_Mixin (_Sticky_Mixin_) :
    """Mixin to reset the attribute to the default value whenever the tool
       user enters an empty value.
    """

    def _check_sanity (self, attr_type, e_type) :
        self.__super._check_sanity (attr_type, e_type)
        if not (TFL.callable (self.computed_default) or self.raw_default) :
            raise TypeError \
                ("%s is sticky but lacks `default`" % (attr_type, ))
    # end def _check_sanity

# end class Sticky_Mixin

class _Id_Entity_Reference_Mixin_ (_EPK_Mixin_) :

    def __delete__ (self, obj) :
        ### We need to manually set the value to None first in order to
        ### get the dependencies updated
        self._set_cooked_value  (obj, None)
        self.__super.__delete__ (obj)
    # end def __delete__

    def _register (self, obj, value) :
        if value is not obj :
            value.register_dependency (obj)
            obj.object_referring_attributes [value].append (self)
    # end def _register

    def _unregister (self, obj, old_value) :
        old_value.unregister_dependency (obj)
        try :
            del obj.object_referring_attributes [old_value]
        except KeyError :
            pass
    # end def _unregister

# end class _Id_Entity_Reference_Mixin_

class Id_Entity_Reference_Mixin (_Id_Entity_Reference_Mixin_) :
    """Kind mixin for handling object references correctly."""

    def _check_sanity (self, attr_type, e_type) :
        if __debug__ :
            if not attr_type.P_Type :
                raise TypeError \
                    ("%s needs to define `P_Type`" % attr_type)
        self.__super._check_sanity (attr_type, e_type)
    # end def _check_sanity

    def _set_cooked_value (self, obj, value, changed = 42) :
        old_value = self.get_value (obj)
        changed   = old_value is not value
        scope_p   = obj._home_scope is not None
        if changed :
            if old_value and scope_p :
                self._unregister (obj, old_value)
            self.__super._set_cooked_value (obj, value, changed)
            if value :
                if obj.init_finished :
                    self._register (obj, value)
                else :
                    obj._init_pending.append \
                        (TFL.Functor (self._register, obj, value))
    # end def _set_cooked_value

# end class Id_Entity_Reference_Mixin

### XXX Object-Reference- and Link-related kinds

__doc__ = """
Class `MOM.Attr.Kind`
============================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: Kind

    `MOM.Attr.Kind` is the root class of a hierarchy of classes defining the
    various kinds of attributes of essential classes. The attribute kind
    controls how the value of an attribute is accessed and how (and if) it
    can be modified. Technically, `Kind` and its subclasses define Python
    `data descriptors` that implement `property` semantics.

    The kind of a concrete attribute is specified as one the properties of
    the :class:`attribute's type<_MOM._Attr.Type.A_Attr_Type>`. The kind
    class gets instantiated by :class:`~_MOM._Attr.Spec.Spec` which passes
    the `type` to the kind's `__init__`.

    Some kinds of attributes are stored into the database, e.g.,
    :class:`Primary`, :class:`Necessary`, :class:`Optional` (and its
    descendents), and :class:`Internal`, others are not, e.g., the various
    kinds of cached and computed attributes.

    There are some mixins that can modify the semantics of :class:`Optional`
    attributes.

.. autoclass:: Primary
.. autoclass:: Primary_Optional
.. autoclass:: Required
.. autoclass:: Necessary
.. autoclass:: Optional

.. autoclass:: Internal
.. autoclass:: Cached
.. autoclass:: Computed
.. autoclass:: Query
.. autoclass:: Auto_Cached
.. autoclass:: Sync_Cached
.. autoclass:: Once_Cached
.. autoclass:: Const

.. autoclass:: Computed_Mixin
.. autoclass:: Computed_Set_Mixin
.. autoclass:: Init_Only_Mixin
.. autoclass:: Sticky_Mixin

"""

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Kind)
    )

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
### __END__ MOM.Attr.Kind
