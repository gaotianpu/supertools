#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import web

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

host = '192.168.1.111'
db = 'plants'
user = 'root'
pw = 'root'


# 基于如下设计：
#http://www.ruanyifeng.com/blog/2010/12/php_best_practices.html
#
source_dir = '/Users/gaotianpu/github/wdc/plants/php/'

dbr = web.database(dbn='mysql', host=host, db=db, user=user, pw=pw)

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

def gen_config(dir):
    li = []
    li.append('<?php')
    li.append('class Config {')
    li.append('public static $conn = new PDO("mysql:host=%s;dbname=%s","%s","%s");' % (host,db,user,pw) )
    li.append('')
    li.append('')
    li.append('')
    li.append('')
    li.append('')
    li.append('')
    li.append('')
    li.append('}')
    li.append('?>')

    lfile = '%sconfig.inc' % (dir)
    save_file(lfile,li)

def gen_basic(dir):
    li = []
    li.append('<?php')     
    li.append('global $ROOT=$_SERVER["DOCUMENT_ROOT"];')
    li.append('require_once("$ROOT/lib/config.inc");')

    tables = load_tables()
    for t in tables:
        className = formatTableName(t) 
        li.append('require_once("$ROOT/lib/model/%s.inc");' % (className) )
    
    for t in tables:
        className = '%sDAO' % (formatTableName(t) )
        li.append('require_once("$ROOT/lib/dao/%s.inc");' % (className) )

    li.append('')
    li.append('')
    li.append('')
    li.append('')
    li.append('')
   
    li.append('?>')

    lfile = '%sbase.inc' % (dir)
    save_file(lfile,li)


formatTableName = lambda table_name: ''.join([x.capitalize() for x in table_name.split('_')]) 
def gen_model(dir):
    tables = load_tables()
    for t in tables:
        className = formatTableName(t) 
        fields = load_fields(t) 

        li = []
        li.append('<?php')
        li.append('class %s {' % (className) )
        for f in fields:
            li.append('var $%s;'%(f.Field))
                

        # li.append('var %s;' % (','.join('$%s' % (f.Field)  for f in fields)  ) ) #$id, $first_name, $last_name, $email
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

        li.append('function save(&$vo) { if ($vo->pk_id == 0) { $this->insert($vo); } else { $this->update($vo); } }')

        li.append('function get($pk_id) {')        
        li.append('$sql = "select * from %s where pk_id=:pk_id";'%(t))
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
        li.append('$r = $result->fetchAll();')  #len?
        for f in fields:
            li.append('$vo->%s = $r[0]["%s"];' % (f.Field,f.Field)  )        
        li.append('}') 

        li.append('function update(&$vo) {')
        # fields1 =  ','.join(['%s=:%s'%(f.Field,f.Field)  for f in fields if f.Field not in ['pk_id','create_date']])
        # fields1 = fields1.replace(':create_date','now()').replace(':last_update','now()')
        # fields2 =  ','.join(['  ' %(f.Field,f.Field)  for f in fields if f.Field not in ['pk_id','create_date','last_update']]) 

        li.append('$fields = array();')
        li.append('$arr = array(":pk_id"=>$vo->pk_id);')
        for f in fields:
            if f.Field not in ['pk_id','create_date','last_update']:
                li.append('if(!is_null($vo->%s)){$arr[":%s"] = $vo->%s;$fields[]="%s=:%s";  }' % (f.Field,f.Field,f.Field,f.Field,f.Field)   )
        
        if 'last_update' in [f.Field for f in fields]:
            li.append('$fields[]="last_update=now()";')

        li.append('$sql = "update %s set ". join(",",$fields) ." where pk_id=:pk_id";' % (t))
        li.append('$p = $this->conn->prepare($sql);')
        li.append('$p->execute($arr);' )
        li.append('$p->rowCount();  ')
        
        li.append('}')

        li.append('function insert(&$vo) {')
        fields3 =  ','.join([f.Field for f in fields if f.Field!='pk_id'])
        fields4 =  ','.join([':%s' %(f.Field)  for f in fields if f.Field!='pk_id'])
        fields4 = fields4.replace(':create_date','now()').replace(':last_update','now()').replace(':status','0')
        fields5 =  ','.join(['":%s"=>$vo->%s' %(f.Field,f.Field)  for f in fields if f.Field not in ['pk_id','create_date','last_update','status']])
        li.append('$sql = "insert into %s (%s) values(%s)";' %(t,fields3,fields4) )
        li.append('$p = $this->conn->prepare($sql);')
        li.append('$p->execute(array(%s));' % fields5 )
        li.append('$vo->pk_id = $this->conn->lastinsertid();  ');
        li.append('}')



        li.append('}') 
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

    gen_config(lib_dir)
    gen_basic(lib_dir)
    
    gen_model(model_lib_dir) 
    gen_dao(dao_lib_dir) 



if __name__ == '__main__':
    run()





    