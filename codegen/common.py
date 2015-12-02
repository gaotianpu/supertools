#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import os
from config import host,db,user,pw

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

dbr = web.database(dbn='mysql', host=host, db=db, user=user, pw=pw)

def load_tables(): 
    results =  list(dbr.query('show tables'))      
    return [t['Tables_in_%s'%(db)] for t in results]
    

def load_fields(table_name):
    # r.Field,r.Type,r.Null,r.Key,r.Default,r.Extra 
    return list(dbr.query('show columns from %s'%(table_name)))
    

def save_file(lfile,li):
    if os.path.exists(lfile): 
        # os.system('cp -f %s %s.bak' % (lfile,lfile) ) 
        os.system('rm -f %s' % (lfile) )

    print '\r\n'.join(li)+'\r\n'
    with open(lfile,'w') as f:
        f.write('\r\n'.join(li)+'\r\n')
        f.close()

if __name__ == "__main__":
    print load_tables()