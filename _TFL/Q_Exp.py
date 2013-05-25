# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer All rights reserved
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
#    TFL.Q_Exp
#
# Purpose
#    Query expression language
#
# Revision Dates
#     4-Dec-2009 (CT) Creation
#     7-Dec-2009 (CT) `Base.undef` and `Bin.undefs` added and used
#    10-Dec-2009 (CT) `Bin.__nonzero__` defined to raise a `TypeError` to
#                     avoid `Q.a < Q.b < Q.c` silently discarding `Q.a <`
#    10-Dec-2009 (CT) `Exp_B` added (and `_Exp_` factored),
#                     and used as base for `Bin_Bool`
#     9-Feb-2010 (CT) Support for queries of nested attributes added
#    10-Feb-2010 (CT) `ENDSWITH` and `STARTSWITH` changed to *not* use
#                     unbound methods of `str` (fail for unicode values, duh)
#    10-Feb-2010 (MG) Converted `lambda` in `startswith` and `endswith` to
#                     functions which have aproper `__name__` which is needed
#                     by the SA instrumentation
#    12-Feb-2010 (CT) `__nonzero__` added to `Base`, `Call`, and `_Exp_`
#     1-Sep-2010 (CT) Reflected binary operators added (__radd__ and friends)
#     2-Sep-2010 (CT) `Get.name`  changed to `Get._name` (ditto for
#                     `Get.getter`)
#    14-Dec-2010 (CT) `Exp.D`, `Exp.DT`, and `Q._Date_` added
#    14-Jan-2011 (CT) Common base `Q_Root` added to all query classes
#    14-Jan-2011 (CT) `Bin` and `__binary` changed to honor `reverse`
#    22-Jul-2011 (CT) `__call__` factored up to `Q_Root`
#    22-Jul-2011 (CT) `LOWER` (and `Func`) added
#    13-Sep-2011 (CT) All internal classes renamed to `_<<name>>_`
#    14-Sep-2011 (CT) `SUM` added
#    16-Sep-2011 (MG) `_SUM_._name` added
#    21-Sep-2011 (CT) `BETWEEN` changed to guard against `val is None`
#    22-Dec-2011 (CT) Change `_Bin_.__repr__` to honor `reverse`
#    22-Feb-2013 (CT)  Use `TFL.Undef ()` not `object ()`
#    25-Feb-2013 (CT) Change `_Get_.predicate` to set `Q.undef.exc`
#    ��revision-date�����
#--

"""
Module `Q_Exp`
===============

This module implements a query expression language::

    >>> from _TFL.Record import Record as R
    >>> from datetime import date, datetime
    >>> r1 = R (foo = 42, bar = 137, baz = 11, quux = R (a = 1, b = 200))
    >>> r2 = R (foo = 3,  bar = 9,   qux = "abcdef", d = date (2010, 12, 14), dt = datetime (2010, 12, 14, 11, 36))
    >>> r3 = R (foo = 42, bar = "AbCd", baz = "ABCD", qux = "abcd")
    >>> q0 = Q.foo
    >>> q0._name
    'foo'
    >>> q0.predicate (r1)
    42

    >>> q1 = Q.foo == Q.bar
    >>> q1, q1.lhs, q1.rhs, q1.op.__name__
    (Q.foo == Q.bar, Q.foo, Q.bar, '__eq__')
    >>> q1.lhs._name, q1.rhs._name
    ('foo', 'bar')
    >>> q1.predicate (r1)
    False

    >>> q2 = Q.foo + Q.bar
    >>> q2, q2.lhs, q2.rhs, q2.op.__name__
    (Q.foo + Q.bar, Q.foo, Q.bar, '__add__')
    >>> q2.predicate (r1)
    179

    >>> q3 = Q.foo % Q.bar == Q.baz
    >>> q3, q3.lhs, q3.rhs
    (Q.foo % Q.bar == Q.baz, Q.foo % Q.bar, Q.baz)
    >>> q3.predicate (r1)
    False
    >>> q4 = Q.bar % Q.foo
    >>> q4.predicate (r1), Q.baz.predicate (r1)
    (11, 11)
    >>> (q4 == Q.baz).predicate (r1)
    True
    >>> q3.lhs.predicate (r1)
    42

    >>> q5 = Q.foo.BETWEEN (10, 100)
    >>> q5, q5.lhs, q5.args, q5.op.__name__
    (Q.foo.between (10, 100), Q.foo, (10, 100), 'between')
    >>> q5.predicate (r1)
    True
    >>> q5.predicate (r2)
    False

    >>> q6 = Q.foo.IN ((1, 3, 9, 27))
    >>> q6.predicate (r1)
    False
    >>> q6.predicate (r2)
    True

    >>> QQ = Q.__class__ (Ignore_Exception = (AttributeError, ))
    >>> QQ.qux.predicate (r1) is QQ.undef
    True
    >>> Q.qux.predicate (r1) is Q.undef
    Traceback (most recent call last):
      ...
    AttributeError: qux

    >>> q7 = QQ.qux.CONTAINS ("bc")
    >>> q7.predicate (r1)
    >>> q7.predicate (r2)
    True
    >>> q8 = QQ.qux.ENDSWITH ("fg")
    >>> q8.predicate (r1)
    >>> q8.predicate (r2)
    False
    >>> q9 = QQ.qux.ENDSWITH ("ef")
    >>> q9.predicate (r1)
    >>> q9.predicate (r2)
    True
    >>> qa = QQ.qux.STARTSWITH ("abc")
    >>> qa.predicate (r1)
    >>> qa.predicate (r2)
    True

    >>> Q [0] ((2,4))
    2
    >>> Q [1] ((2,4))
    4
    >>> Q [-1] ((2,4))
    4
    >>> Q [-2] ((2,4))
    2

    >>> Q.foo * -1
    Q.foo * -1
    >>> -1 * Q.foo
    -1 * Q.foo

    >>> qm = Q.foo.D.MONTH (2, 2010)
    >>> qm, qm.lhs, qm.op.__name__
    (Q.foo.between (datetime.date(2010, 2, 1), datetime.date(2010, 2, 28)), \
        Q.foo, 'between')

    >>> Q.foo.D.MONTH (2, 2000)
    Q.foo.between (datetime.date(2000, 2, 1), datetime.date(2000, 2, 29))

    >>> Q.foo.DT.QUARTER (4, 2010)
    Q.foo.between (datetime.datetime(2010, 10, 1, 0, 0), \
      datetime.datetime(2010, 12, 31, 23, 59, 59))

    >>> Q.foo.D.YEAR (2011)
    Q.foo.between (datetime.date(2011, 1, 1), datetime.date(2011, 12, 31))
    >>> Q.foo.DT.YEAR (2012)
    Q.foo.between (datetime.datetime(2012, 1, 1, 0, 0), \
        datetime.datetime(2012, 12, 31, 23, 59, 59))

    >>> Q.d.D.MONTH (12, 2010) (r2)
    True
    >>> Q.d.D.MONTH (1, 2010) (r2)
    False
    >>> Q.d.D.QUARTER (4, 2010) (r2)
    True
    >>> Q.dt.D.QUARTER (4, 2010) (r2)
    Traceback (most recent call last):
      ...
    TypeError: can't compare datetime.datetime to datetime.date
    >>> Q.dt.DT.QUARTER (4, 2010) (r2)
    True

    >>> Q.bar.LOWER.STARTSWITH ("ab")
    Q.bar.lower ().startswith ('ab',)

    >>> (Q.bar == Q.baz) (r3)
    False
    >>> (Q.bar.LOWER == Q.baz.LOWER) (r3)
    True
    >>> Q.bar (r3), Q.bar.LOWER (r3)
    ('AbCd', 'abcd')
    >>> Q.bar.STARTSWITH ("ab") (r3)
    False
    >>> Q.bar.LOWER.STARTSWITH ("ab") (r3)
    True
    >>> Q.bar.LOWER.STARTSWITH ("bc") (r3)
    False
    >>> Q.bar.CONTAINS ("bc") (r3)
    False
    >>> Q.bar.LOWER.CONTAINS ("bc") (r3)
    True

Python handles `a < b < c` as `(a < b) and (b < c)`. Unfortunately, there is
no way to simulate this by defining operator methods. Therefore,
`_Bin_.__nonzero__` raises a TypeError to signal that an expression like
`Q.a < Q.b < Q.c` isn't possible::

    >>> Q.a < Q.b < Q.c # doctest:+ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: ...

    >>> Q.bar.LOWER == Q.baz.LOWER == Q.qux.LOWER # doctest:+ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: ...

Query operators with boolean results, i.e., equality and ordering operators,
cannot be used with any operators except `==` and `!=`::

    >>> (Q.a < Q.b) < Q.c
    Traceback (most recent call last):
      ...
    TypeError: Operator `<` not applicable to boolean result of `Q.a < Q.b`, rhs: `Q.c`

    >>> Q.a < Q.b + Q.c
    Q.a < Q.b + Q.c
    >>> Q.z + Q.a < Q.b + Q.c
    Q.z + Q.a < Q.b + Q.c
    >>> (Q.a < Q.b) == (Q.a % 2)
    Q.a < Q.b == Q.a % 2
    >>> (Q.a < Q.b) == (Q.a > 2)
    Q.a < Q.b == Q.a > 2
    >>> q = (Q.a < Q.b) == (Q.a % 2)
    >>> q.lhs
    Q.a < Q.b
    >>> q.rhs
    Q.a % 2
    >>> q.op
    <built-in function __eq__>

But explicit parenthesis are necessary in some cases::

    >>> Q.a < Q.b == Q.a % 2 # doctest:+ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: ...

Queries for nested attributes are also possible::

    >>> qn = Q.quux.a
    >>> qn._name
    'quux.a'
    >>> qn.predicate (r1)
    1
    >>> qm = Q.quux.b
    >>> qm.predicate (r1)
    200
    >>> (qn > Q.foo) (r1)
    False
    >>> (qm > Q.foo) (r1)
    True

Q.SUM needs documenting::

    >>> print (Q.SUM (1))
    Q.SUM (1)
    >>> print (Q.SUM (Q.finish - Q.start))
    Q.SUM (Q.finish - Q.start)

    >>> Q.SUM (1) (r1)
    1
    >>> Q.SUM (42) (r1)
    42
    >>> Q.SUM (Q.bar - Q.foo)  (r1)
    95
    >>> Q.SUM (Q.foo - Q.bar)  (r1)
    -95

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

"""

from   __future__  import print_function

from   _TFL                     import TFL
from   _TFL                     import pyk

import _TFL._Meta.Object
import _TFL.Accessor
import _TFL.Decorator
import _TFL.Undef

from   _TFL.predicate           import callable

import operator

@pyk.adapt__bool__
class Base (TFL.Meta.Object) :
    """Query generator"""

    class Ignore_Exception (Exception) : pass

    undef = TFL.Undef ("value")

    def __init__ (self, Ignore_Exception = None) :
        if Ignore_Exception is not None :
            self.Ignore_Exception = Ignore_Exception
    # end def __init__

    def SUM (self, rhs = 1) :
        return self._Sum_ (self, rhs)
    # end def SUM

    def __getattr__ (self, name) :
        if "." in name :
            getter = getattr (TFL.Getter, name)
        else :
            getter = operator.attrgetter (name)
        return self._Get_ (self, name, getter)
    # end def __getattr__

    def __getitem__ (self, item) :
        assert not isinstance (item, slice)
        return self._Get_ (self, item, operator.itemgetter (item))
    # end def __getitem__

    def __bool__ (self) :
        return TypeError \
            ("Result of `%s` cannot be used in a boolean context" % (self, ))
    # end def __bool__

# end class Base

Q = Base ()

class Q_Root (TFL.Meta.Object) :
    """Base class for all classes modelling queries"""

    def __call__ (self, obj) :
        return self.predicate (obj)
    # end def __call__

# end class Q_Root

@TFL.Add_New_Method (Base)
@pyk.adapt__bool__
@pyk.adapt__div__
class _Bin_ (Q_Root) :
    """Binary query expression"""

    op_map               = dict \
        ( __add__        = "+"
        , __truediv__    = "/"
        , __eq__         = "=="
        , __ge__         = ">="
        , __gt__         = ">"
        , __le__         = "<="
        , __lt__         = "<"
        , __mod__        = "%"
        , __mul__        = "*"
        , __rmul__       = "*"
        , __pow__        = "**"
        , __sub__        = "-"
        )

    rop_map              = dict \
        ( __radd__       = "__add__"
        , __rdiv__       = "__truediv__"
        , __rmod__       = "__mod__"
        , __rmul__       = "__mul__"
        , __rpow__       = "__pow__"
        , __rsub__       = "__sub__"
        )

    predicate_precious_p = True

    def __init__ (self, lhs, op, rhs, undefs, reverse = False) :
        self.Q       = lhs.Q
        self.lhs     = lhs
        self.op      = op
        self.rhs     = rhs
        self.undefs  = undefs
        self.reverse = reverse
    # end def __init__

    def predicate (self, obj) :
        l = self.lhs.predicate (obj)
        try :
            pred = self.rhs.predicate
        except AttributeError :
            r = self.rhs
        else :
            r = pred (obj)
        if not any ((v is u) for v in (l, r) for u in self.undefs) :
            ### Call `op` only if neither `l` nor `v` is an undefined value
            if self.reverse :
                l, r = r, l
            return self.op (l, r)
    # end def predicate

    def __bool__ (self) :
        return TypeError \
            ("Result of `%s` cannot be used in a boolean context" % (self, ))
    # end def __bool__

    def __repr__ (self) :
        op = self.op.__name__
        lhs, rhs = self.lhs, self.rhs
        if self.reverse :
            lhs, rhs = rhs, lhs
        return "%s %s %s" % (lhs, self.op_map.get (op, op), rhs)
    # end def __repr__

# end class _Bin_

@TFL.Add_New_Method (Base)
@pyk.adapt__bool__
class _Call_ (Q_Root) :
    """Query expression calling a method."""

    predicate_precious_p = True

    def __init__ (self, lhs, op, * args, ** kw) :
        self.Q      = lhs.Q
        self.lhs    = lhs
        self.op     = op
        self.args   = args
        self.kw     = kw
    # end def __init__

    def predicate (self, obj) :
        l = self.lhs.predicate (obj)
        if l is not self.Q.undef :
            return self.op (l, * self.args, ** self.kw)
    # end def predicate

    def __bool__ (self) :
        return TypeError \
            ("Result of `%s` cannot be used in a boolean context" % (self, ))
    # end def __bool__

    def __repr__ (self) :
        op = self.op.__name__
        return "%s.%s %r" % (self.lhs, op, self.args)
    # end def __repr__

# end class _Call_

def __binary (op, Class) :
    name    = op.__name__
    reverse = name in _Bin_.rop_map
    key     = _Bin_.rop_map [name] if reverse else name
    op      = getattr (operator, key)
    if name in ("__eq__", "__ne__") :
        ### Allow `x == None` and `x != None`
        undefs = (Q.undef, )
    else :
        ### Ignore `None` for all other operators
        undefs = (None, Q.undef)
    def _ (self, rhs) :
        return getattr (self.Q, Class) (self, op, rhs, undefs, reverse)
    _.__doc__    = op.__doc__
    _.__name__   = name
    _.__module__ = op.__module__
    return _
# end def __binary

def _binary (op) :
    return __binary (op, "_Bin_Expr_")
# end def _binary

def _boolean (op) :
    return __binary (op, "_Bin_Bool_")
# end def _boolean

def _method (meth) :
    name = meth.__name__
    op   = meth ()
    def _ (self, * args, ** kw) :
        return self.Q._Call_ (self, op, * args, ** kw)
    _.__doc__    = op.__doc__
    _.__name__   = name
    _.__module__ = meth.__module__
    return _
# end def _method

def _type_error (op) :
    name = op.__name__
    def _ (self, rhs) :
        raise TypeError \
            ( "Operator `%s` not applicable to boolean result of `%s`"
              ", rhs: `%s`"
            % (_Bin_.op_map.get (name, name), self, rhs)
            )
    _.__doc__    = op.__doc__
    _.__name__   = name
    _.__module__ = op.__module__
    return _
# end def _type_error

@TFL.Add_New_Method (Base)
class _Date_ (TFL.Meta.Object) :

    class Date (TFL.Meta.Object) :

        import datetime

        type       = datetime.date
        lom_delta  = datetime.timedelta (days=1)

    # end class Date

    class Date_Time (TFL.Meta.Object) :

        import datetime

        type       = datetime.datetime
        lom_delta  = datetime.timedelta (seconds=1)

    # end class Date_Time

    def __init__ (self, exp, D_Type) :
        self.exp    = exp
        self.D_Type = D_Type
    # end def __init__

    def MONTH (self, m, y) :
        D_Type = self.D_Type
        m      = int (m)
        y      = int (y)
        if m < 12 :
            n  = m + 1
            z  = y
        else :
            n  = 1
            z  = y + 1
        lhs    = D_Type.type (y, m, 1)
        rhs    = D_Type.type (z, n, 1) - D_Type.lom_delta
        return self.exp.BETWEEN (lhs, rhs)
    # end def MONTH

    def QUARTER (self, q, y) :
        D_Type = self.D_Type
        q      = int (q)
        y      = int (y)
        m      = 1 + 3 * (q - 1)
        if q < 4 :
            n  = m + 3
            z  = y
        else :
            n  = 1
            z  = y + 1
        lhs    = D_Type.type (y, m, 1)
        rhs    = D_Type.type (z, n, 1) - D_Type.lom_delta
        return self.exp.BETWEEN (lhs, rhs)
    # end def QUARTER

    def YEAR (self, y) :
        D_Type = self.D_Type
        y      = int (y)
        return self.exp.BETWEEN \
            ( D_Type.type (y,   1, 1)
            , D_Type.type (y+1, 1, 1) - D_Type.lom_delta
            )
    # end def YEAR

# end class _Date_

@pyk.adapt__bool__
class _Exp_Base_ (Q_Root) :

    ### Equality queries
    @_boolean
    def __eq__ (self, rhs) : pass

    @_boolean
    def __ne__ (self, rhs) : pass

    def __hash__ (self) :
        ### Override `__hash__` just to silence DeprecationWarning:
        ###     Overriding __eq__ blocks inheritance of __hash__ in 3.x
        raise NotImplementedError
    # end def __hash__

    def __bool__ (self) :
        return TypeError \
            ("Result of `%s` cannot be used in a boolean context" % (self, ))
    # end def __bool__

# end class _Exp_Base_

class _Exp_ (_Exp_Base_) :
    """Query expression"""

    ### Order queries
    @_boolean
    def __ge__ (self, rhs) : pass

    @_boolean
    def __gt__ (self, rhs) : pass

    @_boolean
    def __le__ (self, rhs) : pass

    @_boolean
    def __lt__ (self, rhs) : pass

    ### Binary non-boolean queries
    @_binary
    def __add__ (self, rhs) : pass

    @_binary
    def __truediv__ (self, rhs) : pass

    @_binary
    def __mod__ (self, rhs) : pass

    @_binary
    def __mul__ (self, rhs) : pass

    @_binary
    def __pow__ (self, rhs) : pass

    @_binary
    def __sub__ (self, rhs) : pass

    ### Binary non-boolean reflected queries
    @_binary
    def __radd__ (self, rhs) : pass

    @_binary
    def __rdiv__ (self, rhs) : pass

    @_binary
    def __rmod__ (self, rhs) : pass

    @_binary
    def __rmul__ (self, rhs) : pass

    @_binary
    def __rpow__ (self, rhs) : pass

    @_binary
    def __rsub__ (self, rhs) : pass

    ### Method calls
    @_method
    def BETWEEN () :
        def between (val, lhs, rhs) :
            """between(val, lhs, rhs) -- Returns result of `lhs <= val <= rhs`"""
            return val is not None and lhs <= val <= rhs
        return between
    # end def BETWEEN

    @_method
    def CONTAINS () :
        return operator.contains
    # end def CONTAINS

    @property
    def D (self) :
        return self.Q._Date_ (self, self.Q._Date_.Date)
    # end def D

    @property
    def DT (self) :
        return self.Q._Date_ (self, self.Q._Date_.Date_Time)
    # end def DT

    @_method
    def ENDSWITH () :
        def endswith (l, r) :
            return l.endswith (r)
        return endswith
    # end def ENDSWITH

    @_method
    def IN () :
        def in_ (val,  rhs) :
            """in_(val, lhs) -- Returns result of `val in rhs`"""
            return val in rhs
        return in_
    # end def IN

    @property
    def LOWER (self) :
        def lower (val) :
            return val.lower ()
        return self.Q._Func_ (self, lower)
    # end def LOWER

    @_method
    def STARTSWITH () :
        def startswith (l, r) :
            return l.startswith (r)
        return startswith
    # end def STARTSWITH

# end class _Exp_

@pyk.adapt__div__
class _Exp_B_ (_Exp_Base_) :
    """Query expression for query result of type Boolean"""

    ### Order queries
    @_type_error
    def __ge__ (self, rhs) : pass

    @_type_error
    def __gt__ (self, rhs) : pass

    @_type_error
    def __le__ (self, rhs) : pass

    @_type_error
    def __lt__ (self, rhs) : pass

    ### Binary non-boolean queries
    @_type_error
    def __add__ (self, rhs) : pass

    @_type_error
    def __truediv__ (self, rhs) : pass

    @_type_error
    def __mod__ (self, rhs) : pass

    @_type_error
    def __mul__ (self, rhs) : pass

    @_type_error
    def __pow__ (self, rhs) : pass

    @_type_error
    def __sub__ (self, rhs) : pass

    ### Binary non-boolean reflected queries
    @_type_error
    def __radd__ (self, rhs) : pass

    @_type_error
    def __rdiv__ (self, rhs) : pass

    @_type_error
    def __rmod__ (self, rhs) : pass

    @_type_error
    def __rmul__ (self, rhs) : pass

    @_type_error
    def __rpow__ (self, rhs) : pass

    @_type_error
    def __rsub__ (self, rhs) : pass

# end class _Exp_B_

@TFL.Add_New_Method (Base)
class _Func_ (_Exp_, _Call_) :
    """Query function with a result that can be used in query expressions."""

# end class _Func_

@TFL.Add_New_Method (Base)
class _Get_ (_Exp_) :
    """Query getter"""

    predicate_precious_p = True

    def __init__ (self, Q, name, getter) :
        self.Q       = Q
        self._name   = name
        self._getter = getter
    # end def __init__

    def predicate (self, obj) :
        Q = self.Q
        try :
            return self._getter (obj)
        except Q.Ignore_Exception as exc :
            Q.undef.exc = exc
            return Q.undef
    # end def predicate

    def SET (self, obj, value) :
        name = self._name
        if "." in name :
            head, name = name.rsplit (".", 1)
            obj = getattr (TFL.Getter, head) (obj)
        setattr (obj, name, value)
    # end def SET

    def __getattr__ (self, name) :
        full_name = ".".join ((self._name, name))
        getter    = getattr (TFL.Getter, full_name)
        return self.__class__ (self.Q, full_name, getter)
    # end def __getattr__

    def __repr__ (self) :
        return "Q.%s" % (self._name, )
    # end def __repr__

# end class _Get_

@TFL.Add_New_Method (Base)
class _Q_Exp_Bin_Bool_ (_Bin_, _Exp_B_) :
    """Binary query expression evaluating to boolean"""

    _real_name = "_Bin_Bool_"

_Bin_Bool_ = _Q_Exp_Bin_Bool_ # end class

@TFL.Add_New_Method (Base)
class _Q_Exp_Bin_Expr_ (_Bin_, _Exp_) :
    """Binary query expression"""

    _real_name = "_Bin_Expr_"

_Bin_Expr_ = _Q_Exp_Bin_Expr_ # end class

@TFL.Add_New_Method (Base)
class _Sum_ (Q_Root) :
    """Query function for building a sum."""

    _name = "$SUM"

    def __init__ (self, Q, rhs = 1) :
        self.Q     = Q
        self.rhs   = rhs
    # end def __init__

    def predicate (self, obj) :
        try :
            pred   = self.rhs.predicate
        except AttributeError :
            result = self.rhs
        else :
            result = pred (obj)
        return result
    # end def predicate

    def __repr__ (self) :
        return "Q.SUM (%r)" % (self.rhs, )
    # end def __repr__

# end class _Sum_

if __name__ != "__main__" :
    TFL._Export ("Q")
    TFL._Export_Module ()
### __END__ TFL.Q_Exp
