#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from common import load_tables,load_fields,save_file
from config import host,db,user,pw,source_dir

# 基于如下设计：
#http://www.ruanyifeng.com/blog/2010/12/php_best_practices.html
#

private_dir = '%sprivate/' % (source_dir)
public_dir ='%spublic/' % (source_dir)

common_lib_dir = '%scommon/'%(private_dir)
model_lib_dir = '%smodel/'%(private_dir)
dao_lib_dir = '%sdao/'%(private_dir)
logic_lib_dir = '%slogic/'%(private_dir)
control_dir = '%scontroller/'%(private_dir)
templates_dir = '%stemplates/'%(private_dir)
admin_dir = '%sadmin/'%(source_dir)

static_dir = '%sstatic/'%(public_dir)  #/static/favio.icon,logo.png, lib-zip.js? 
js_dir = '%s/js/'%(static_dir)
css_dir = '%s/css/'%(static_dir) 
img_dir = '%s/img/'%(static_dir) 
font_dir = '%s/fonts/'%(static_dir) 

def mkdir():
    os.system('mkdir %s' % (source_dir) )      
    os.system('mkdir %s' % (private_dir) )  
    os.system('mkdir %s' % (public_dir) )   

    os.system('mkdir %s' % (static_dir) )   
    os.system('mkdir %s' % (js_dir) )   
    os.system('mkdir %s' % (css_dir) )   
    os.system('mkdir %s' % (img_dir) )   
    os.system('mkdir %s' % (font_dir) )     

    os.system('mkdir %s'%(source_dir)) 
    os.system('mkdir %s' % (common_lib_dir))
    os.system('mkdir %s' % (model_lib_dir))
    os.system('mkdir %s' % (dao_lib_dir))
    os.system('mkdir %s' % (logic_lib_dir))
    os.system('mkdir %s' % (control_dir))
    os.system('mkdir %s' % (templates_dir) ) 

    os.system('cp -R ./static/. %s' % (static_dir) )
    os.system('cp -R ./templates/php/BaseDAO.inc %sBaseDAO.inc.gen' % (dao_lib_dir) ) 
    os.system('cp -R ./templates/php/index.php %sindex.php.gen' % (public_dir) ) 

 
def gen_config(dir):
    li = []
    li.append('<?php') 
    li.append('class Config {')   
    li.append("static $dbRinfo = ['dsn'=>'mysql:host=%s;dbname=%s;port=3306;charset=utf8', " % (host,db))    
    li.append("'username' => '%s','password' => '%s' ];" % (user,pw))

    li.append("static $dbWinfo = ['dsn'=>'mysql:host=%s;dbname=%s;port=3306;charset=utf8', " % (host,db) )    
    li.append("'username' => '%s','password' => '%s' ];" % (user,pw))

    li.append('}')
    li.append('?>')

    lfile = '%sconfig.inc.gen' % (dir)
    save_file(lfile,li)

def gen_basic(dir):
    li = []
    li.append('<?php')   
    li.append('require_once(ROOT_DIR."/private/dao/BaseDAO.inc");')  
    li.append('require_once(ROOT_DIR."/private/controller/BaseController.inc");')   

    tables = load_tables()
    for t in tables:
        className = formatTableName(t) 
        li.append('require_once(ROOT_DIR."/private/model/%s.inc");' % (className) )
        li.append('require_once(ROOT_DIR."/private/dao/%s.inc");' % ('%sDAO' % ( className )) )
        li.append('require_once(ROOT_DIR."/private/logic/%s.inc");' % ( '%sLogic' % ( className ) ) )     
        li.append('') 
    li.append('?>')

    lfile = '%sbase.inc.gen' % (dir)
    save_file(lfile,li)


formatTableName = lambda table_name: ''.join([x.capitalize() for x in table_name.split('_')]) 
def _gen_model(dir,t,fields):
    className = formatTableName(t) 
   

    li = []
    li.append('<?php')
    li.append('class %s {' % (className) )
    for f in fields:
        li.append('var $%s;'%(f.Field))            

    # li.append('var %s;' % (','.join('$%s' % (f.Field)  for f in fields)  ) ) #$id, $first_name, $last_name, $email
    li.append('}')
    li.append('?>')

    lfile = '%s%s.inc.gen' % (dir,className)
    save_file(lfile,li)


def _gen_dao(dir,t,fields):
    className = '%sDAO' % (formatTableName(t) ) 

    li = []
    li.append('<?php')     
    li.append('class %s extends BaseDAO {' % (className)) 

    li.append('function save(&$vo) { if ($vo->pk_id == 0) { $this->insert($vo); } else { $this->update($vo); } }')

    li.append('function get($pk_id) {')  

    li.append('$sql = "select %s from %s where pk_id=:pk_id";'%(','.join([f.Field for f in fields]),t))
    li.append('$p = $this->dbR->prepare($sql);')
    li.append('$p->execute(array(":pk_id"=>$pk_id));')
    li.append('$vo = new %s();' % ( formatTableName(t) )  )  
    li.append('$this->getFromResult($vo,$p) ; ') 
    li.append('return $vo;')      
    li.append('}')

    li.append('function delete(&$vo) {')
    li.append('$sql = "update %s set status=1 where pk_id=:pk_id ";' % (t))
    li.append('$p = $this->dbR->prepare($sql);')
    li.append('$p->execute(array(":pk_id"=>$vo->pk_id));')
    li.append('$p->rowCount(); ')
    li.append('}') 

    li.append('#-- private functions')
    li.append('function getFromResult(&$vo, $result) {')
    li.append('if(($r = $result->fetch(PDO::FETCH_ASSOC)) !== false){')  #len?
    for f in fields:
        li.append('$vo->%s = $r["%s"];' % (f.Field,f.Field)  )        
    li.append('}}') 

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
    li.append('$p = $this->dbW->prepare($sql);')
    li.append('$p->execute($arr);' )
    li.append('$p->rowCount();  ')
    
    li.append('}')

    li.append('function insert(&$vo) {')
    fields3 =  ','.join([f.Field for f in fields if f.Field!='pk_id'])
    fields4 =  ','.join([':%s' %(f.Field)  for f in fields if f.Field!='pk_id'])
    fields4 = fields4.replace(':create_date','now()').replace(':last_update','now()').replace(':status','0')
    fields5 =  ','.join(['":%s"=>$vo->%s' %(f.Field,f.Field)  for f in fields if f.Field not in ['pk_id','create_date','last_update','status']])
    li.append('$sql = "insert into %s (%s) values(%s)";' %(t,fields3,fields4) )
    li.append('$p = $this->dbW->prepare($sql);')
    li.append('$p->execute(array(%s));' % fields5 )
    li.append('$vo->pk_id = $this->dbW->lastinsertid();  ');
    li.append('}')


    li.append('}') 
    li.append('?>')

    lfile = '%s%s.inc.gen' % (dir,className)
    save_file(lfile,li)
        


def _gen_logic(logic_lib_dir,t,fields): 
    className = '%sLogic' % (formatTableName(t) )
     
    li = []
    li.append('<?php') 
    li.append('class %s {' % (className))

    li.append('}') 
    li.append('?>')

    lfile = '%s%s.inc.gen' % (logic_lib_dir,className)
    save_file(lfile,li)       


        
def _gen_controller(control_dir,t,fields):
    className = '%sController' % (formatTableName(t) )
    
    li = []
    li.append('<?php') 
    li.append('class %s {' % (className))
    
    li.append('}') 
    li.append('?>')

    lfile = '%s%s.inc.gen' % (control_dir,className)
    save_file(lfile,li)


def gen_parts(parts_dir):
    # header,footer,sidebar
    tables = load_tables()
    for t in tables:
        className = '%sPage' % (formatTableName(t) )
        fields = load_fields(t)
        li = []
        li.append('<?php') 
         
        li.append('?>')

        lfile = '%s%s.inc.gen' % (parts_dir,className)
        save_file(lfile,li)

def gen_phpfile(source_dir):    
    for page in ['index','login','register','getpwd','photo']:
        li = []
        li.append('<?php') 
        li.append('?>')
        lfile = '%s%s.php' % (source_dir,page)
        # save_file(lfile,li)

    tables = load_tables()
    for t in tables:
        className = '%s' % (formatTableName(t) )
        fields = load_fields(t)
        li = []
        li.append('<?php') 
        li.append('?>')
        lfile = '%s%s.php' % (source_dir,className)
        # save_file(lfile,li)

def gen_model(dir):
    tables = load_tables()
    for t in tables:
        _gen_model(dir,t)

def gen_dao(dir):
    tables = load_tables()
    for t in tables:
        _gen_dao(dir,t)

def gen_logic(logic_lib_dir):
    tables = load_tables()
    for t in tables:
        _gen_logic(logic_lib_dir,t)

def gen_controller(control_dir):
    tables = load_tables()
    for t in tables:        
        _gen_controller(control_dir,t)

 
def gen_all_tables():
    tables = load_tables()
    for t in tables:
        gen_table(t) 

def gen_table(t):
    className = formatTableName(t) 
    fields = load_fields(t) 
    _gen_model(model_lib_dir,t,fields)
    _gen_dao(dao_lib_dir,t,fields)
    _gen_logic(logic_lib_dir,t,fields)


def run():   
    mkdir() 
    gen_config(private_dir)
    gen_basic(private_dir)     
    gen_all_tables() 

    # gen_parts(templates_dir)
    # gen_phpfile(source_dir) 

  
if __name__ == '__main__':    
    # run() 
    gen_table('upload_batches')





    