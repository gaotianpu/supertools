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

host = '127.0.0.1'
db = 'plants'
user = 'root'
pw = 'root'
source_dir = '/Users/gaotianpu/github/wdc/plants/php/'
private_dir = '%sprivate/' % (source_dir)
public_dir ='%spublic/' % (source_dir)

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
    li.append('define("DB_HOST", "mysql:host=%s;dbname=%s");' % (host,db) )
    li.append('define("DB_USER","%s");'%(user))
    li.append('define("DB_PWD","%s");'%(pw))
    li.append('')
    li.append('')
    li.append('')
    # li.append('}')
    li.append('?>')

    lfile = '%sconfig.inc' % (dir)
    save_file(lfile,li)

def gen_basic(dir):
    li = []
    li.append('<?php')      

    tables = load_tables()
    for t in tables:
        className = formatTableName(t) 
        li.append('require_once($ROOT_DIR."/private/model/%s.inc");' % (className) )
    
    for t in tables:
        className = '%sDAO' % (formatTableName(t) )
        li.append('require_once($ROOT_DIR."/private/dao/%s.inc");' % (className) )

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
        # li.append('require_once("../model/%s.inc");' % (formatTableName(t)) )
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
        li.append('$sql = "update replies set status=1 where pk_id=:pk_id ";')
        li.append('$p = $this->conn->prepare($sql);')
        li.append('$p->execute(array(":pk_id"=>$vo->pk_id));')
        li.append('$p->rowCount(); ')
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

def gen_logic(logic_lib_dir):
    tables = load_tables()
    for t in tables:
        className = '%sLogic' % (formatTableName(t) )
        fields = load_fields(t)
        li = []
        li.append('<?php') 
        li.append('class %s {' % (className))

        li.append('}') 
        li.append('?>')

        lfile = '%s%s.inc' % (logic_lib_dir,className)
        save_file(lfile,li)

def gen_controller(control_dir):
    tables = load_tables()
    for t in tables:
        className = '%sController' % (formatTableName(t) )
        fields = load_fields(t)
        li = []
        li.append('<?php') 
        li.append('class %s {' % (className))
        
        li.append('}') 
        li.append('?>')

        lfile = '%s%s.inc' % (control_dir,className)
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

        lfile = '%s%s.inc' % (parts_dir,className)
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

def run():    
    lib_dir = '%slib/'%(source_dir)

    common_lib_dir = '%scommon/'%(private_dir)
    model_lib_dir = '%smodel/'%(private_dir)
    dao_lib_dir = '%sdao/'%(private_dir)
    logic_lib_dir = '%slogic/'%(private_dir)
    control_dir = '%scontrol/'%(private_dir)
    templates_dir = '%stemplates/'%(private_dir)
    admin_dir = '%sadmin/'%(source_dir)

    static_dir = '%sstatic/'%(public_dir)  #/static/favio.icon,logo.png, lib-zip.js? 
    js_dir = '%s/js/'%(static_dir)
    css_dir = '%s/css/'%(static_dir) 
    img_dir = '%s/img/'%(static_dir) 
    font_dir = '%s/fonts/'%(static_dir) 

    os.system('mkdir %s' % (private_dir) )  
    os.system('mkdir %s' % (public_dir) )   

    os.system('mkdir %s' % (static_dir) )   
    os.system('mkdir %s' % (js_dir) )   
    os.system('mkdir %s' % (css_dir) )   
    os.system('mkdir %s' % (img_dir) )   
    os.system('mkdir %s' % (font_dir) )     

    os.system('mkdir %s'%(source_dir))
    #os.system('mkdir %s' % (lib_dir))
    os.system('mkdir %s' % (common_lib_dir))
    os.system('mkdir %s' % (model_lib_dir))
    os.system('mkdir %s' % (dao_lib_dir))
    os.system('mkdir %s' % (logic_lib_dir))
    os.system('mkdir %s' % (control_dir))
    os.system('mkdir %s' % (templates_dir) )     

    gen_config(private_dir)
    gen_basic(private_dir)    
    gen_model(model_lib_dir) 
    gen_dao(dao_lib_dir) 
    gen_logic(logic_lib_dir)
    gen_controller(control_dir)
    gen_parts(templates_dir)
    gen_phpfile(source_dir)

    os.system('pwd')
    os.system('cp -R ./static/. %s' % (static_dir) )   

#mysqldump -h 192.168.1.111 -uroot -proot --skip-lock-tables database > plants.sql


if __name__ == '__main__':
    run()





    