# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer All rights reserved
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
#    ��revision-date�����
#--

"""
This module implements a query expression language::

    >>> from _TFL.Record import Record as R
    >>> r1 = R (foo = 42, bar = 137, baz = 11)
    >>> q0 = Q.foo
    >>> q0.name
    'foo'
    >>> q0.predicate (r1)
    42

    >>> q1 = Q.foo == Q.bar
    >>> q1, q1.lhs, q1.rhs, q1.op.__name__
    (Q.foo == Q.bar, Q.foo, Q.bar, '__eq__')
    >>> q1.lhs.name, q1.rhs.name
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

    >>> QQ = Q.__class__ (Ignore_Exception = AttributeError)
    >>> QQ.qux.predicate (r1) is QQ.undef
    True
    >>> Q.qux.predicate (r1) is Q.undef
    Traceback (most recent call last):
      ...
    AttributeError: qux

    >>> Q [0] ((2,4))
    2
    >>> Q [1] ((2,4))
    4
    >>> Q [-1] ((2,4))
    4
    >>> Q [-2] ((2,4))
    2

Python handles `a < b < c` as `(a < b) and (b < c)`. Unfortunately, there is
no way to simulate this by defining operator methods. Therefore,
`Bin.__nonzero__` raises a TypeError to signal that an expression like
`Q.a < Q.b < Q.c` isn't possible::

    >>> Q.a < Q.b < Q.c
    Traceback (most recent call last):
      ...
    TypeError: __nonzero__ should return bool or int, returned exceptions.TypeError

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

    >>> Q.a < Q.b == Q.a % 2
    Traceback (most recent call last):
      ...
    TypeError: __nonzero__ should return bool or int, returned exceptions.TypeError

"""

from   _TFL                     import TFL

import _TFL._Meta.Object
import _TFL.Decorator

from   _TFL.predicate           import callable

import operator

class Base (TFL.Meta.Object) :
    """Query generator"""

    class Ignore_Exception (StandardError) : pass

    undef = object ()

    def __init__ (self, Ignore_Exception = None) :
        if Ignore_Exception is not None :
            self.Ignore_Exception = Ignore_Exception
    # end def __init__

    def __getattr__ (self, name) :
        assert "." not in name, name
        return self.Get (self, name, operator.attrgetter (name))
    # end def __getattr__

    def __getitem__ (self, item) :
        assert not isinstance (item, slice)
        return self.Get (self, item, operator.itemgetter (item))
    # end def __getitem__

# end class Base

Q = Base ()

@TFL.Add_New_Method (Base)
class Bin (TFL.Meta.Object) :
    """Binary query expression"""

    op_map        = dict \
        ( __add__ = "+"
        , __div__ = "/"
        , __eq__  = "=="
        , __ge__  = ">="
        , __gt__  = ">"
        , __le__  = "<="
        , __lt__  = "<"
        , __mod__ = "%"
        , __mul__ = "*"
        , __pow__ = "**"
        , __sub__ = "-"
        )

    predicate_precious_p = True

    def __init__ (self, lhs, op, rhs, undefs) :
        self.Q      = lhs.Q
        self.lhs    = lhs
        self.op     = op
        self.rhs    = rhs
        self.undefs = undefs
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
            return self.op (l, r)
    # end def predicate

    def __call__ (self, obj) :
        return self.predicate (obj)
    # end def __call__

    def __nonzero__ (self) :
        return TypeError \
            ("Result of `%s` cannot be used in a boolean context" % (self, ))
    # end def __nonzero__

    def __repr__ (self) :
        op = self.op.__name__
        return "%s %s %s" % (self.lhs, self.op_map.get (op, op), self.rhs)
    # end def __repr__

# end class Bin

@TFL.Add_New_Method (Base)
class Call (TFL.Meta.Object) :
    """Query expression calling a method."""

    predicate_precious_p = True

    def __init__ (self, lhs, op, * args, ** kw) :
        self.Q           = lhs.Q
        self.lhs         = lhs
        self.op          = op
        self.attr_args   = args
        self.attr_kw     = kw
    # end def __init__

    def predicate (self, obj) :
        l = self.lhs.predicate (obj)
        if l is not self.Q.undef :
            return self.op (l, * self.attr_args, ** self.attr_kw)
    # end def predicate

    def __call__ (self, obj) :
        return self.predicate (obj)
    # end def __call__

# end class Call

def __binary (op, Class) :
    name = op.__name__
    op   = getattr (operator, name)
    if name in ("__eq__", "__ne__") :
        ### Allow `x == None` and `x != None`
        undefs = (Q.undef, )
    else :
        ### Ignore `None` for all other operators
        undefs = (None, Q.undef)
    def _ (self, rhs) :
        return getattr (self.Q, Class) (self, op, rhs, undefs)
    _.__doc__    = op.__doc__
    _.__name__   = name
    _.__module__ = op.__module__
    return _
# end def __binary

def _binary (op) :
    return __binary (op, "Bin_Expr")
# end def _binary

def _boolean (op) :
    return __binary (op, "Bin_Bool")
# end def _boolean

def _method (meth) :
    name = meth.__name__
    op   = meth ()
    def _ (self, * args, ** kw) :
        return self.Q.Call (self, op, * args, ** kw)
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
            % (Bin.op_map.get (name, name), self, rhs)
            )
    _.__doc__    = op.__doc__
    _.__name__   = name
    _.__module__ = op.__module__
    return _
# end def _type_error


class _Exp_ (TFL.Meta.Object) :

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

# end class _Exp_

class Exp (_Exp_) :
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
    def __div__ (self, rhs) : pass

    @_binary
    def __mod__ (self, rhs) : pass

    @_binary
    def __mul__ (self, rhs) : pass

    @_binary
    def __pow__ (self, rhs) : pass

    @_binary
    def __sub__ (self, rhs) : pass

    ### Method calls
    @_method
    def between () :
        def between (val, lhs, rhs) :
            """between(val, lhs, rhs) -- Returns result of `lhs <= val <= rhs`"""
            return lhs <= val <= rhs
        return between
    # end def between

    @_method
    def contains () :
        return operator.contains
    # end def contains

    @_method
    def endswith () :
        return str.endswith
    # end def endswith

    @_method
    def in_ () :
        def in_ (val,  rhs) :
            """in_(val, lhs) -- Returns result of `val in rhs`"""
            return val in rhs
        return in_
    # end def in_

    @_method
    def startswith () :
        return str.startswith
    # end def startswith

# end class Exp

class Exp_B (_Exp_) :
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
    def __div__ (self, rhs) : pass

    @_type_error
    def __mod__ (self, rhs) : pass

    @_type_error
    def __mul__ (self, rhs) : pass

    @_type_error
    def __pow__ (self, rhs) : pass

    @_type_error
    def __sub__ (self, rhs) : pass

# end class Exp_B

@TFL.Add_New_Method (Base)
class Get (Exp) :
    """Query getter"""

    predicate_precious_p = True

    def __init__ (self, Q, name, getter) :
        self.Q      = Q
        self.name   = name
        self.getter = getter
    # end def __init__

    def predicate (self, obj) :
        Q = self.Q
        try :
            return self.getter (obj)
        except Q.Ignore_Exception :
            return Q.undef
    # end def predicate

    def __call__ (self, obj) :
        return self.predicate (obj)
    # end def __call__

    def __repr__ (self) :
        return "Q.%s" % self.name
    # end def __repr__

# end class Get

@TFL.Add_New_Method (Base)
class _Q_Exp_Bin_Bool_ (Bin, Exp_B) :
    """Binary query expression evaluating to boolean"""

    _real_name = "Bin_Bool"

Bin_Bool = _Q_Exp_Bin_Bool_ # end class

@TFL.Add_New_Method (Base)
class _Q_Exp_Bin_Expr_ (Bin, Exp) :
    """Binary query expression"""

    _real_name = "Bin_Expr"

Bin_Expr = _Q_Exp_Bin_Expr_ # end class

if __name__ != "__main__" :
    TFL._Export ("Q")
    TFL._Export_Module ()
### __END__ TFL.Q_Exp
