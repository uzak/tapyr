# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008-2009 Martin Gl�ck All rights reserved
# Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
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
#    DJO.Apps.Base.templatetags.TGL_Filters
#
# Purpose
#    Tanzer and Glueck's library of custom django template filters
#
# Revision Dates
#     9-May-2008 (MG) Creation (factored from TGL_Tags)
#     9-May-2008 (MG) Arithmetic and bool filters added
#    12-May-2008 (MG) `sequence_filter` added
#    12-May-2008 (MG) `sequence_filter`: support `None` as passed in sequence
#    14-May-2008 (CT) Use `_define_op_filter` instead of `exec`
#    17-Oct-2008 (CT) `allow_user` added
#    14-May-2009 (CT) Moved to `_DJO._Apps.Base`
#    15-May-2009 (CT) Alphabetic sequence
#    15-May-2009 (CT) `tel_uri` added
#    ��revision-date�����
#--

"""
>>> from django.conf     import settings
>>> settings.configure (ROOT_URLCONF = "_DJO._test_url_conf")
>>> from django.template import add_to_builtins, Template, Context
>>> add_to_builtins ("_DJO._Apps.Base.templatetags.TGL_Filters")
>>> template = '''
...   {{ var|starts_with:"foo"  }}
...   {{ var|starts_with:"fooa" }}
...   {{ var|starts_with:"afoo" }}
...   {{ var|starts_with:"fo"   }}
... '''
>>> t = Template (template)
>>> t.render (Context (dict (var = "foo"))).strip ()
u'True\\n  False\\n  False\\n  True'
>>> t.render (Context (dict (var = ""))).strip ()
u''

>>> template = '''
...   {{ var|eq:"1"}} {{ var|ne:"1"}} {{ var|eq:bar}} {{ var|ne:bar}}
... '''
>>> t = Template (template)
>>> t.render (Context (dict (var = 1, bar = 1))).strip ()
u'False True True False'
>>> t.render (Context (dict (var = "1", bar = 1))).strip ()
u'True False False True'
>>> template = '''
...   {{ var|gt:1}} {{ var|gt:bar}} {{ var|gt:3 }}
...   {{ var|ge:1}} {{ var|ge:bar}} {{ var|ge:3 }}
...   {{ var|lt:1}} {{ var|lt:bar}} {{ var|lt:3 }}
...   {{ var|le:1}} {{ var|le:bar}} {{ var|le:3 }}
... '''
>>> t = Template (template)
>>> t.render (Context (dict (var = 2, bar = 2))).strip ()
u'True False False\\n  True True False\\n  False False True\\n  False True True'
>>> template = '''
...   {{ var|add:1}} {{  var|sub:bar }}
...   {{ var|mul:2}} {{  var|div:bar }}
...   {{ var|mod:2}} {{  var|pow:bar }}
...   {{ var|mod:3}} {{ nvar|abs     }} {{ var|abs}}
... '''
>>> t = Template (template)
>>> t.render (Context (dict (var = 20, bar = 2, nvar = -10))).strip ()
u'21 18\\n  40 10\\n  0 400\\n  2 10 20'

>>> from _TFL.Record import Record as R
>>> seq = R (hidden = True,  text = "A"), R (hidden = False,  text = "B"), R (hidden = True,  text = "C")
>>> [r.text for r in sequence_filter (seq, "hidden:True")]
['A', 'C']
>>> [r.text for r in sequence_filter (seq, "hidden")]
['A', 'C']
>>> [r.text for r in sequence_filter (seq, "hidden:False")]
['B']
>>> [r.text for r in sequence_filter (None, "hidden:True")]
[]

>>> template = '''
...   For registration, please call {{ "+43-1-234-56-78"|tel_uri }}.'''
>>> t = Template (template)
>>> t.render (Context ()).strip ()
u'For registration, please call <a href="tel:+43-1-234-56-78">+43-1-234-56-78</a>.'
>>> template = '''
...   For registration, please call {{ "+43-1-234-56-78"|tel_uri:"M. Mouse" }}.'''
>>> t = Template (template)
>>> t.render (Context ()).strip ()
u'For registration, please call <a href="tel:+43-1-234-56-78">M. Mouse</a>.'

"""

from   _TFL.Decorator              import Attributed

from   django.template             import defaultfilters
from   django                      import template
import operator

register = template.Library ()

@register.filter
def allow_user (page, user) :
    """Returns true if `page` allows access to `user`."""
    if user and hasattr (page, "allow_user") :
        return page.allow_user (user)
    return True
# end def allow_user

@register.filter
def sequence_filter (sequence, filter_spec) :
    if sequence :
        attr, condition = filter_spec, True
        if ":" in filter_spec :
            attr, condition = (p.strip () for p in filter_spec.split (":", 1))
            try :
                condition = eval (condition, {})
            except :
                pass
        return (e for e in sequence if getattr (e, attr, False) == condition)
    return ()
# end def sequence_filter

@register.filter
@defaultfilters.stringfilter
def starts_with (value, prefix) :
    """Returns the result of `value.startswith (prefix)`"""
    return value and value.startswith (prefix)
# end def starts_with

@Attributed (is_safe = True)
@register.filter
@defaultfilters.stringfilter
def tel_uri (phone_number, text=None) :
    """Returns a telephone URI for `phone_number`.

       http://tools.ietf.org/html/rfc3966
    """
    if text is None :
        text = phone_number
    return u"""<a href="tel:%(phone_number)s">%(text)s</a>""" % locals ()
# end def tel_uri

### Ideally, we'd just pass `getattr (operator, op)` to register.filter
### but the unfortunate `inspect.getargspec` throws a sissy fit
###   >>> from inspect import getargspec
###   >>> getargspec (abs)
###   Traceback (most recent call last):
###     ...
###   TypeError: arg is not a Python function

def _define_op_filter (name) :
    op = getattr (operator, name)
    def _ (lhs, rhs) :
        return op (lhs, rhs)
    register.filter (name, _)

for op in \
        ( "eq",  "ge",  "gt",  "le",  "lt",  "ne"
        , "add", "div", "mod", "mul", "pow", "sub"
        ) :
    _define_op_filter (op)

@register.filter
def abs (value) :
    return operator.abs (value)
# end def abs

### __END__ DJO.Apps.Base.templatetags.TGL_Filters
