# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002-2009 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Meta.Object
#
# Purpose
#    Base class using TFL.Meta.Class as metaclass
#
# Revision Dates
#    13-May-2002 (CT) Creation
#    17-Jan-2003 (CT) `M_` prefixes added
#    24-Mar-2003 (CT) Delegation for `__init__` added
#     5-Mar-2008 (CT) `_TFL_Meta_Object_Root_` added to accomodate Python 2.6
#                     (http://bugs.python.org/issue1683368)
#     2-Feb-2009 (CT) Documentation improved
#    17-Jul-2009 (CT) `_check_MRO` and doctest added to `_TFL_Meta_Object_Root_`
#    ��revision-date�����
#--

from   _TFL import TFL
import _TFL._Meta.M_Class

class _TFL_Meta_Object_Root_ (object) :
    """Root class to fix `__init__` and `__new__`.

       As of Python 2.6, `object.__init__` doesn't accept parameters
       (http://bugs.python.org/issue1683368).

       Don't inherit from _TFL_Meta_Object_Root_ directly(unless you really
       know what you're doing).

       >>> class A (object) :
       ...     def __init__ (self, x = 2) :
       ...         print "A.__init__:", x
       ...         self.x = x
       ...         super (A, self).__init__ ()
       ...
       >>> class B (TFL.Meta.Object, A) :
       ...     def __init__ (self, y) :
       ...         print "B.__init__:", y
       ...         self.y = y
       ...         self.__super.__init__ ()
       ...
       >>> b = B (1)
       Traceback (most recent call last):
           ...
       AssertionError: MRO conflict for B.__init__: super != object,
           (<class 'Object.B'>, <class 'Object.Object'>, <class 'Object._TFL_Meta_Object_Root_'>, <class 'Object.A'>, <type 'object'>)
       >>> class C (object) :
       ...     def __init__ (self, x = 2) :
       ...         print "C.__init__:", x
       ...         self.x = x
       ...         super (C, self).__init__ ()
       ...
       >>> class D (TFL.Meta.Object, C) :
       ...     def __init__ (self, y, x = 3) :
       ...         print "D.__init__:", y
       ...         self.y = y
       ...         self.__super.__init__ (y = y, x = x)
       ...         C.__init__ (self, x)
       ...     @classmethod
       ...     def _check_MRO (cls, args, kw) :
       ...         '''We know what we're doing and explicitly call `C__init__`.'''
       ...
       >>> d = D (42)
       D.__init__: 42
       C.__init__: 3
       >>> print d.x,d.y
       3 42
    """

    def __new__ (cls, * args, ** kw) :
        if __debug__ :
            cls._check_MRO (args, kw)
        return object.__new__ (cls)
    # end def __new__

    def __init__ (self, * args, ** kw) :
        object.__init__ (self)
    # end def __init__

    @classmethod
    def _check_MRO (cls, args, kw) :
        if (args or kw) :
            ### Make sure that there is not class intervening between
            ### `_TFL_Meta_Object_Root_` and `object` in `cls.__mro__`
            ###
            ### due to http://bugs.python.org/issue1683368, cooperative
            ### calls to `__new__` and `__init__` can't work **unless**
            ### all cooperating classes derive from the same root (that
            ### is not `object`)
            sup = super (_TFL_Meta_Object_Root_, cls)
            msg       = \
                ( "MRO conflict for %s.%%s: super != object,\n    %s"
                % (cls.__name__, cls.__mro__)
                )
            assert sup.__new__  is object.__new__,  (msg % ("__new__", ))
            assert sup.__init__ is object.__init__, (msg % ("__init__", ))
    # end def _check_MRO

# end class _TFL_Meta_Object_Root_

class _TFL_Meta_Object_ (_TFL_Meta_Object_Root_) :
    """Instead of `object`, `TFL.Meta.Object` should be used as baseclass to
       define top-level classes. Classes derived (directly or indirectly)
       from `Object` gain the benefits:

       - :class:`~_TFL._Meta.M_Class.M_Class` is used as metaclass unless an
         explicit metaclass is defined for the derived class. `M_Class`
         provides the benefits:

         * `__super` for cooperative method calls
           (see :class:`~_TFL._Meta.M_Class.M_Autosuper`).

         * Renaming to `_real_name` to avoid name clashes between classes in
           a class hierarchy (see :class:`~_TFL._Meta.M_Class.M_Autorename`).

         * Adding of the properties listed in `__properties`
           (see :class:`~_TFL._Meta.M_Class.M_Autoproperty`).

         Even if an explicit metaclass is defined for a class, it should
         still derive from `Object` to gain protection for cooperative
         `__init__` and `__new__` calls.

       - Cooperative super-calls to `__init__` (and `__new__`) are protected
         against `object.__init__` not accepting parameters in Python 2.6 and
         later.

         * More general, some, if not all, future incompatibility problems
           are easy to solve if `Object` is the single ancestor in
           need of fixing.
    """

    __metaclass__ = TFL.Meta.M_Class
    """TFL.Meta.M_Class is used as metaclass for this class and all its
       dependents (which don't override the metaclass)
       """

    _real_name    = "Object"
    """This class will be known and used as `Object` although the class
       statement contains a different (mangled) name. This allows the use of
       the generic class name `Object` in different packages without messing
       up Python's name mangling. The renaming is done by `TFL.Meta.M_Class`
       (more specifically, by `TFL.Meta.M_Autorename` which is one of the
       bases of `M_Class`).
       """

    __properties  = []
    """`TFL.Meta.M_Autoproperty` will add and initialize all elements of
       `__properties` automatically. These should be instances of
       `TFL.Meta.Property` or one of its descendents (or signature compatible
       with it).

       `TFL.Meta.M_Autoproperty` is *not* a metaclass of this class.
       Descendent classes needing `M_Autoproperty` need to specify
       `TFL.Meta.M_Class_SWRP` as metaclass.
       """

    def __init__ (self, * args, ** kw) :
        ### delegate to `__super` to accomodate multiple inheritance
        self.__super.__init__ (* args, ** kw)
    # end def __init__

Object = _TFL_Meta_Object_ # end class

if __name__ != "__main__" :
    TFL.Meta._Export ("Object")
### __END__ TFL.Meta.Object
