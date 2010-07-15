# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package MOM.DBW.SAS.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW.SAS.Pid_Manager
#
# Purpose
#    SAS specific manager for permanent ids
#
# Revision Dates
#    11-May-2010 (MG) Creation
#    12-May-2010 (MG) Support for PostgreSQL sequences added
#    17-May-2010 (CT) `reserve` changed to `insert` for postgresql, too
#    17-May-2010 (MG) `new_context` replaced by `context`
#    24-Jun-2010 (CT) `commit`, `reserve`, and `rollback` factored to `dbs`
#     1-Jul-2010 (MG) `max_pid` and `__iter__` added, `type_name` factored
#    15-Jul-2010 (MG) `close` added
#    ��revision-date�����
#--

from   _MOM       import MOM
from   _TFL       import TFL

import _MOM._DBW._HPS
import _MOM._DBW.Pid_Manager

class Pid_Manager (MOM.DBW.Pid_Manager) :
    """SAS specific manager for permanent ids."""

    def __init__ (self, ems, db_url) :
        self.__super.__init__ (ems, db_url)
        sa_table     = self.ems.DBW.sa_pid
        self.insert  = sa_table.insert ()
        self.select  = sa_table.select ()
        self.pid_col = sa_table.c.pid
        self.tn_col  = sa_table.c.Type_Name
        self.dbs     = self.ems.DBW.DBS_map [db_url.scheme]
    # end def __init__

    def commit (self) :
        self.dbs.commit_pid (self)
    # end def commit

    @TFL.Meta.Once_Property
    def connection (self) :
        result           = self.ems.session.engine.connect ()
        self.transaction = result.begin                    ()
        return result
    # end def connection

    @TFL.Contextmanager
    def context (self, entity, pid) :
        try :
            yield self (entity, pid, commit = False)
        except :
            self.rollback ()
            raise
        else :
            self.commit   ()
    # end def new_context

    def close (self) :
        self.rollback         ()
        self.connection.close ()
    # end def close

    @property
    def max_pid (self) :
        result = self.connection.execute \
            (self.select.limit (1).order_by (self.pid_col.desc ()))
        row = result.fetchone ()
        if row :
            return row.pid
        return 0
    # end def max_pid

    def new (self, entity, commit = True) :
        Type_Name = None
        if entity :
            Type_Name = entity.type_name
        sql    = self.insert.values      (Type_Name = Type_Name)
        result = self.connection.execute (sql)
        if commit :
            self.commit ()
        pid = int (result.inserted_primary_key [0])
        if entity :
            entity.pid = pid
        return pid
    # end def new

    def query (self, pid) :
        try :
            type_name = self.type_name (pid)
            return self.ems.scope [type_name].query (pid = pid).one ()
        except StandardError :
            raise LookupError ("No object with pid `%d` found" % (pid, ))
    # end def query

    def reserve (self, entity, pid, commit = True) :
        self.dbs.reserve_pid (self.connection, pid)
        Type_Name = None
        if entity :
            Type_Name  = entity.type_name
            entity.pid = pid
        sql    = self.insert.values      (Type_Name = Type_Name, pid = pid)
        result = self.connection.execute (sql)
        if commit :
            self.commit ()
        return pid
    # end def reserve

    def rollback (self) :
        if self.transaction :
            self.dbs.rollback_pid (self)
    # end def rollback

    def type_name (self, pid) :
        result = self.connection.execute \
            (self.select.where (self.pid_col == pid))
        found  = result.fetchone ()
        self.commit              ()
        if found and found.type_name :
            return found.type_name
        raise LookupError ("No object with pid `%d` found" % (pid, ))
    # end def type_name

    def __iter__ (self) :
        result = self.connection.execute \
            (self.select.order_by (self.pid_col.asc ()))
        for row in result :
            if row.type_name :
                yield row.pid, row.type_name
    # end def __iter__

# end class Pid_Manager

if __name__ != "__main__" :
    MOM.DBW.SAS._Export ("*")
### __END__ MOM.DBW.SAS.Pid_Manager
