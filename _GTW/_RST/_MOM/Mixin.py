# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.MOM.
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
#    GTW.RST.MOM.Mixin
#
# Purpose
#    Define mixin classes for GTW.RST.MOM
#
# Revision Dates
#    22-Jun-2012 (CT) Creation
#     3-Jul-2012 (CT) Factored from _GTW/_RST/MOM.py
#     3-Jul-2012 (CT) Add support for `Query_Restriction`
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource
import _GTW._RST.HTTP_Method
import _GTW._RST._MOM.Query_Restriction

from   _MOM.import_MOM          import MOM, Q

from   _TFL._Meta.Once_Property import Once_Property
import _TFL._Meta.Object

class _PUT_POST_Mixin_ (GTW.RST.HTTP_Method) :

    failure_code = 400 ### Bad request

    def _request_attr (self, resource, request, response) :
        try :
            result = request.json ["attributes"]
        except KeyError :
            raise ValueError \
                ("""You need to send the attributes defining """
                 """the object with the request """
                 """(content-type "application/json")"""
                )
        else :
            attributes = set   (a.name for a in resource.E_Type.edit_attr)
            invalids   = tuple (k for k in result if k not in attributes)
            if invalids :
                raise ValueError \
                    ( "Request contains invalid attribute names "
                    + repr (invalids)
                    )
        return result
    # end def _request_attr

    def _response_body (self, resource, request, response) :
        try :
            attrs = self._request_attr (resource, request, response)
            obj   = self._apply_attrs  (resource, request, response, attrs)
        except Exception as exc :
            resource.scope.rollback ()
            response.status_code = self.failure_code
            result               = dict (error = str (exc))
        else :
            resource.scope.commit ()
            response.status_code = self.success_code
            e      = resource._new_entry (obj.pid)
            result = e.GET ()._response_body (e, request, response)
        return result
    # end def _response_body

# end class _PUT_POST_Mixin_

class RST_Mixin (TFL.Meta.Object) :
    """Mixin for MOM-specific RST classes."""

    _attributes                = None
    _change_info               = None
    _sort_key_cid_reverse      = TFL.Sorted_By ("-cid")

    @Once_Property
    def E_Type (self) :
        ETM = self._ETM
        if isinstance (ETM, basestring) :
            result = self.top.App_Type [ETM]
        else :
            result = ETM.E_Type
        return result
    # end def E_Type

    @Once_Property
    def ETM (self) :
        result = self._ETM
        if isinstance (result, basestring) :
            result = self.top.scope [result]
        return result
    # end def ETM

    @property
    def attributes (self) :
        result = self._attributes
        if result is None :
            result = self._attributes = self.E_Type.edit_attr
        return result
    # end def attributes

    @attributes.setter
    def attributes (self, value) :
        def _gen (vs) :
            E_Type = self.E_Type
            for v in vs :
                if isinstance (v, basestring) :
                    v = getattr (E_Type, v)
                yield v
        self._attributes = tuple (_gen (value)) if value is not None else None
    # end def attributes

    @property
    def change_info (self) :
        result = self._change_info
        if result is None :
            result = self._change_info = self._get_change_info ()
        return result
    # end def change_info

    def query_changes (self) :
        scope = self.top.scope
        cqfs   = self.change_query_filters
        if cqfs is not None :
            return scope.query_changes \
                (* cqfs).order_by (self._sort_key_cid_reverse)
    # end def query_changes

    def _get_change_info (self) :
        result = None
        qc     = self.query_changes ()
        if qc is not None :
            lc = qc.first ()
            if lc is not None :
                result = TFL.Record \
                    ( cid           = lc.cid
                    , etag          = "ET-%s-%s" % (lc.time, lc.cid)
                    , last_modified = lc.time.replace (microsecond = 0)
                    )
        return result
    # end def _get_change_info

    @TFL.Contextmanager
    def _handle_method_context (self, method, request) :
        with self.__super._handle_method_context (method, request) :
            with self.LET (_change_info = self._get_change_info ()) :
                yield
    # end def _prepare_handle_method

# end class RST_Mixin

class RST_E_Type_Mixin (RST_Mixin) :
    """Mixin for classes of E_Type classes."""

    QR                         = GTW.RST.MOM.Query_Restriction

    default_qr_kw              = dict ()
    query_restriction          = None
    sort_key                   = None

    _last_change               = None
    _objects                   = []
    _old_cid                   = -1

    objects                    = property (lambda s : s._get_objects ())

    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "ETM", prefix = "_")
        if "name" not in kw :
            kw ["name"] = self.E_Type.type_name.replace (".", "-")
        self.__super.__init__ (** kw)
    # end def __init__

    @property
    def count (self) :
        if self.query_filters :
            result = self.query ().count ()
        else :
            result = self.ETM.count
        return result
    # end def count

    @Once_Property
    def change_query_filters (self) :
        result = ()
        E_Type = self.E_Type
        if E_Type.is_partial :
            if E_Type.type_name != "MOM.Id_Entity" :
                result = (Q.type_name.IN (sorted (E_Type.children_np)), )
        else :
            result = (Q.type_name == E_Type.type_name, )
        return result
    # end def change_query_filters

    @Once_Property
    def query_filters (self) :
        return tuple ()
    # end def query_filters

    def query (self, sort_key = None) :
        result = self.ETM.query \
            (* self.query_filters, sort_key = sort_key or self.sort_key)
        if self.query_restriction is not None :
            result = self.query_restriction (result)
        return result
    # end def query

    def _get_objects (self) :
        change_info = self.change_info
        cid = change_info and change_info.cid
        if  self._old_cid != cid :
            self._old_cid  = cid
            self._objects = self.query ().all ()
        return self._objects
    # end def _get_objects

    @TFL.Contextmanager
    def _handle_method_context (self, method, request) :
        with self.__super._handle_method_context (method, request) :
            qr = self.QR.from_request \
                (self.E_Type, request, ** self.default_qr_kw)
            kw = dict (query_restriction = qr)
            if qr :
                if qr.attributes :
                    kw ["attributes"] = qr.attributes
                ### temporarily invalidate cache
                kw.update (_old_cid = object (), _objects = [])
            with self.LET (** kw) :
                yield
    # end def _prepare_handle_method

# end class RST_E_Type_Mixin

if __name__ != "__main__" :
    GTW.RST.MOM._Export ("*", "_PUT_POST_Mixin_")
### __END__ GTW.RST.MOM.Mixin