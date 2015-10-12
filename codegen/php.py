#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import web

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


# 基于如下设计：
#http://www.ruanyifeng.com/blog/2010/12/php_best_practices.html
#
source_dir = '/Users/gaotianpu/github/wdc/plants/php/'

dbr = web.database(dbn='mysql', host='192.168.1.111', db='plants', user='root', pw='root')

def load_tables():    
    return [t.Tables_in_plants for t in list(dbr.query('show tables'))]
    

def load_fields(table_name):
    return list(dbr.query('show columns from %s'%(table_name)))
    # r.Field,r.Type,r.Null,r.Key,r.Default,r.Extra 

def save_file(lfile,li):
    if os.path.exists(lfile): 
        os.system('cp -f %s %s.bak' % (lfile,lfile) ) 
        os.system('rm -f %s' % (lfile) )

    print '\r\n'.join(li)+'\r\n'
    with open(lfile,'w') as f:
        f.write('\r\n'.join(li)+'\r\n')
        f.close()

formatTableName = lambda table_name: ''.join([x.capitalize() for x in table_name.split('_')]) 

def gen_model(dir):
    tables = load_tables()
    for t in tables:
        className = formatTableName(t) 
        fields = load_fields(t) 

        li = []
        li.append('<?php')
        li.append('class %s {' % (className) )
        li.append('var %s;' % (','.join('$%s' % (f.Field)  for f in fields)  ) ) #$id, $first_name, $last_name, $email
        li.append('}')
        li.append('?>')

        lfile = '%s%s.inc' % (dir,className)
        save_file(lfile,li)

        
def gen_dao(dir):
    tables = load_tables()
    for t in tables:
        className = '%sDAO' % (formatTableName(t) )
        fields = load_fields(t)

        li = []
        li.append('<?php')
        li.append('require_once("../model/%s.inc");' % (formatTableName(t)) )
        li.append('class %s {' % (className))

        li.append('var $conn;')
        li.append('function %s(& $conn) {$this->conn =&$conn;}' % (className) )

        li.append('function save(&$vo) { if ($v->pk_id == 0) { $this->insert($vo); } else { $this->update($vo); } }')

        li.append('function get($pk_id) {')        
        li.append('$sql = "select * from users where pk_id=:pk_id";')
        li.append('$p = $this->conn->prepare($sql);')
        li.append('$p->execute(array(":pk_id"=>$pk_id));')
        li.append('$vo = new %s();' % ( formatTableName(t) )  )  
        li.append('$this->getFromResult($vo,$p) ; ') 
        li.append('return $vo;')      
        li.append('}')

        li.append('function delete(&$vo) {')
        li.append('}') 

        li.append('#-- private functions')
        li.append('function getFromResult(&$vo, $result) {')
        li.append('$r = $result->fetchAll();')
        for f in fields:
            li.append('$vo->%s = $r[0]["%s"];' % (f.Field,f.Field)  )        
        li.append('}') 

        li.append('function update(&$vo) {')
        li.append('}')

        li.append('function insert(&$vo) {')
        li.append('}')

        li.append('}')

        # test
        li.append('$conn  = new PDO("mysql:host=192.168.1.111;dbname=plants","root","root");')
        li.append('$dao = new %s($conn);'%(className))
        li.append('$result = $dao -> get(1);')
        li.append('print_r($result);')

        li.append('?>')

        lfile = '%s%s.inc' % (dir,className)
        save_file(lfile,li)


def run():    
    lib_dir = '%slib/'%(source_dir)
    common_lib_dir = '%slib/common/'%(source_dir)
    model_lib_dir = '%slib/model/'%(source_dir)
    dao_lib_dir = '%slib/dao/'%(source_dir)
    logic_lib_dir = '%slib/logic/'%(source_dir)
    parts_dir = '%sparts/'%(source_dir)
    control_dir = '%scontrol/'%(source_dir)

    os.system('mkdir %s'%(source_dir))
    os.system('mkdir %s' % (lib_dir))
    os.system('mkdir %s' % (common_lib_dir))
    os.system('mkdir %s' % (model_lib_dir))
    os.system('mkdir %s' % (dao_lib_dir))
    os.system('mkdir %s' % (logic_lib_dir))
    os.system('mkdir %s' % (parts_dir)   )  
    os.system('mkdir %s' % (control_dir))
    
    gen_model(model_lib_dir) 
    gen_dao(dao_lib_dir) 


if __name__ == '__main__':
    run()





    