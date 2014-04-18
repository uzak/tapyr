# -*- coding: utf-8 -*-
# Copyright (C) 2009-2014 Mag. Christian Tanzer All rights reserved
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
#    JNJ.GTW
#
# Purpose
#    Provide additional global functions for Jinja templates
#
# Revision Dates
#    29-Dec-2009 (CT) Creation
#    13-Jan-2010 (CT) Converted to class; `call_macro` added;
#                     `_T` and `_Tn` added to class `GTW`
#    25-Jan-2010 (MG) `_T` and `_Tn` need to be static methods
#    27-Jan-2010 (CT) `Getter`, `now`, and `sorted` added
#    17-Feb-2010 (CT) `email_uri`, `obfuscated`, `tel_uri`, and `uri` added
#    23-Feb-2010 (CT) `pjoin` added
#    24-Feb-2010 (CT) `log_stdout` added
#    10-Mar-2010 (CT) `zip` added
#     3-May-2010 (MG) `call_macro`: `widget_type` added
#     5-May-2010 (MG) `render_fofi_widget` added
#     5-May-2010 (MG) `default_render_mode` used
#     5-May-2010 (MG) `render_mode` added
#     6-May-2010 (MG) `render_fofi_widget` exception handling improoved
#     3-Aug-2010 (CT) Use `HTML.obfuscator` instead of home-grown code
#     3-Aug-2010 (CT) `obfuscated` removed
#    20-Sep-2010 (CT) `Sorted_By` added
#    22-Sep-2010 (CT) `eval_sorted_by` added
#     8-Oct-2010 (CT) `len` added
#    23-Nov-2010 (CT) `list` and `reversed` added
#    27-Nov-2010 (CT) `formatted` added
#    18-Mar-2011 (CT) `get_macro` changed to use `Template_E.get_macro`
#    22-Mar-2011 (CT) `dict` added
#    30-Nov-2011 (CT) Add `filtered_join`
#    30-Nov-2011 (CT) Add `dir` and `getattr`
#     1-Dec-2011 (CT) Add `styler`
#    18-Jan-2012 (CT) Add `attr_join`
#    27-Jan-2012 (CT) Change `email_uri` to allow tuple argument for `email`
#    22-Feb-2012 (CT) Add `vimeo_video` and `youtube_video`
#     4-May-2012 (CT) Change `email_uri` to allow email-tuple and `text` passed
#    16-Jul-2012 (MG) `log_stdout` enhanced
#     6-Aug-2012 (MG) Add `update_blackboard`
#     8-Aug-2012 (MG) Remove debug code
#     9-Aug-2012 (MG) Use `** kw` notation for `update_blackboard`
#    12-Feb-2014 (CT) Add `enumerate`
#    13-Feb-2014 (CT) Add `Dingbats` and `unichr`
#    14-Mar-2014 (CT) Add `any` and `all`
#    10-Apr-2014 (CT) Add `first`
#    14-Apr-2014 (CT) Add `ichain`
#    18-Apr-2014 (CT) Add `bool`
#    ««revision-date»»···
#--

from   _JNJ                     import JNJ
from   _TFL                     import TFL

from   _GTW                     import HTML

from   _TFL.pyk                 import pyk
from   _TFL                     import sos
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import filtered_join

from   _TFL._Meta.Once_Property import Once_Property

import _TFL._Meta.Object
import _TFL.Accessor
import _TFL.Sorted_By

import itertools

class GTW (TFL.Meta.Object) :
    """Provide additional global functions for Jinja templates."""

    from jinja2.runtime import Undefined

    def __init__ (self, env) :
        import _JNJ.Templateer ### used by `get_macro`
        self.env               = env
        self.render_mode_stack = []
    # end def __init__

    all  = staticmethod (all)
    any  = staticmethod (any)
    bool = staticmethod (bool)

    @Once_Property
    def Dingbats (self) :
        from _TFL import Dingbats
        return Dingbats
    # end def Dingbats

    def attr_join (self, sep, objects, attr_name) :
        """Join the values of attribute `attr_name` of `objects` by `sep`."""
        def _gen (objects, attr_name) :
            for o in objects :
                a = getattr (o, attr_name)
                if a :
                    yield a
        return sep.join (_gen (objects, attr_name))
    # end def attr_join

    def call_macro (self, macro_name, * _args, ** _kw) :
        """Call macro named by `macro_name` passing `* _args, ** _kw`."""
        templ_name  = _kw.pop ("templ_name",  None)
        widget_type = _kw.pop ("widget_type", None)
        try :
            macro  = self.get_macro (macro_name, templ_name, widget_type)
        except ValueError :
            print repr ((macro_name, templ_name, _args, _kw))
            raise
        return macro (* _args, ** _kw)
    # end def call_macro

    dict = staticmethod (dict)
    dir  = staticmethod (dir)

    def email_uri (self, email, text = None, ** kw) :
        """Returns a mailto URI for `email`.

           http://tools.ietf.org/html/rfc3966
        """
        if isinstance (email, tuple) :
            email, email_text = email
        if text is None :
            text = email_text
        return self.uri (scheme = "mailto", uri = email, text = text, ** kw)
    # end def email_uri

    enumerate = staticmethod (enumerate)

    def eval_sorted_by (self, key = None) :
        """Returns a function that can be passed to `Sorted_By` to evaluate
           the `sorted_by` attribute of an object, If `key` is passed in, the
           `sorted_by` attribute of the attribute referred to by `key` will
           be evaluated.
        """
        if key is None :
            result = lambda obj : obj.sorted_by (obj)
        else :
            getter = getattr (TFL.Getter, key)
            def result (obj) :
                v = getter (obj)
                return v.sorted_by (v)
        return result
    # end def eval_sorted_by

    filtered_join = staticmethod (filtered_join)
    first         = staticmethod (TFL.first)

    def firstof (self, * args) :
        if len (args) == 1 and isinstance (args [0], (tuple, list)) :
            args = args [0]
        for a in args :
            if not (a is None or isinstance (a, self.Undefined)) :
                return a
    # end def firstof

    def formatted (self, format, * args, ** kw) :
        if args :
            assert not kw
            return format % args
        else :
            return format % kw
    # end def formatted

    def get_macro (self, macro_name, templ_name = None, widget_type = None) :
        """Return macro `macro_name` from template `templ_name`."""
        if widget_type :
            macro_name = getattr (macro_name, widget_type)
        if not isinstance (macro_name, basestring) :
            macro_name = str (macro_name)
        if templ_name is None :
            templ_name, macro_name = \
                (p.strip () for p in macro_name.split (",", 1))
        template = self.env.get_template (templ_name)
        if isinstance (template, JNJ.Template_E) :
            result = template.get_macro (macro_name)
        else :
            result = getattr (template.module, macro_name)
        return result
    # end def get_macro

    getattr    = staticmethod (getattr)
    Getter     = TFL.Getter

    ichain     = staticmethod (itertools.chain)
    len        = staticmethod (len)
    list       = staticmethod (list)

    def log_stdout (self, * text) :
        print " ".join (str (l) for l in text)
        return ""
    # end def log_stdout

    def now (self, format = "%Y/%m/%d") :
        from datetime import datetime
        result = datetime.now ()
        return result.strftime (format)
    # end def now

    pjoin      = staticmethod (sos.path.join)

    def render_fofi_widget (self, fofi, widget, * args, ** kw) :
        pushed          = False
        obj_render_mode = getattr (fofi, "render_mode", None)
        kw_render_mode  = kw.pop  ("render_mode",       None)
        if obj_render_mode :
            pushed      = True
            self.render_mode_stack.append (obj_render_mode)
        elif kw_render_mode :
            pushed      = True
            self.render_mode_stack.append (kw_render_mode)
        elif not self.render_mode_stack :
            pushed      = True
            self.render_mode_stack.append (fofi.default_render_mode)
        render_mode     = self.render_mode_stack [-1]
        try :
            try :
                mode_desc = fofi.render_mode_description [render_mode]
            except ValueError :
                raise ValueError \
                    ("%r does not support render mode %r" % (fofi, render_mode))
            result      = self.call_macro \
                (getattr (mode_desc, widget), * args, ** kw)
            return result
        finally :
            if pushed :
                self.render_mode_stack.pop ()
    # end def render_fofi_widget

    @Once_Property
    def render_mode (self) :
        return self.render_mode_stack and self.render_mode_stack [-1]
    # end def render_mode

    reversed   = staticmethod (reversed)
    sorted     = staticmethod (sorted)
    Sorted_By  = TFL.Sorted_By
    styler     = staticmethod (HTML.Styler)

    def tel_uri (self, phone_number, text = None, ** kw) :
        """Returns a telephone URI for `phone_number`.

           http://tools.ietf.org/html/rfc3966
        """
        return self.uri (scheme = "tel", uri = phone_number, text = text, ** kw)
    # end def tel_uri

    def update_blackboard (self, ** kw) :
        self.blackboard.update (kw)
        return ""
    # end def update_blackboard

    unichr = staticmethod (pyk.unichr)

    def uri (self, scheme, uri, text = None, ** kw) :
        obfuscate = kw.pop ("obfuscate", False)
        if text is None :
            text = uri
        attrs = ['href="%s:%s"' % (scheme, uri)]
        for k, v in kw.iteritems () :
            attrs.append ('%s="%s"' % (k, v))
        attrs = " ".join (sorted (attrs))
        result = u"""<a %(attrs)s>%(text)s</a>""" % locals ()
        if obfuscate :
            result = HTML.obfuscator [scheme] (result)
        return result
    # end def uri

    vimeo_video   = staticmethod (HTML.vimeo_video)
    youtube_video = staticmethod (HTML.youtube_video)

    zip           = staticmethod (zip)
    _T            = staticmethod (_T)
    _             = staticmethod (_)
    _Tn           = staticmethod (_Tn)

# end class GTW

if __name__ != "__main__" :
    JNJ._Export ("GTW")
### __END__ JNJ.GTW
