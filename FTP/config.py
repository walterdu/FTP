#coding:utf8
import MySQLdb
import time,os,sys
import SocketServer,getpass
class Mysql:
    def __init__(self,host,user,passwd,db):
        self.host=host
        self.user=user
        self.passwd=passwd
        self.db=db
        try:
            self.conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=3306)
            self.cur=self.conn.cursor()
        except:
            print 'Database connection error'
    def query(self,qtables,qwhere):#Selection Function
        self.qtables=qtables
        self.qwhere=qwhere
        print 'select %s from %s'%(self.qwhere,self.qtables)
        self.cur.execute('select %s from %s'%(self.qwhere,self.qtables))
        self.conn.commit()
        return self.cur.fetchall()
    def new_insert(self,ntable,nwhere,nvalue):#Insert fuction
        self.nwhere=nwhere
        self.ntable=ntable
        self.nvalue=nvalue
        sql='insert into %s(%s) values%s'%(self.ntable,self.nwhere,self.nvalue)
        self.cur.execute(sql)
        self.conn.commit()
    def delete(self,dtables,dwhere):
        self.dtables=dtables
        self.dwhere=dwhere
        self.cur.execute('delete from %s where %s '%(self.dtables,self.dwhere))
        self.conn.commit()
    def update(self,utables,ucolumn,uvalues,uwhere):#Update function
        self.utables=utables
        self.uwhere=uwhere
        self.uvalues=uvalues
        self.ucolumn=ucolumn
        print 'update %s set %s=%s where id=%s'%(self.utables,self.ucolumn,self.uvalues,self.uwhere)
        self.cur.execute("update %s set %s='%s' where id=%s"%(self.utables,self.ucolumn,self.uvalues,self.uwhere))
        self.conn.commit()
    def __del__(self):
        self.cur.close()
        self.conn.close()

con=Mysql('localhost','ftp','123.com','ftp')
def exists(user):#judge whether the username is exsit
    ex_u=con.query("user_info where username='%s'"%user,'id')
    if len(ex_u)==0:
        print "nohava"
        return "no"
    else:
        print "uid"
        print int(ex_u[0][0])
        return int(ex_u[0][0])

#(2L, 'test', '123.com', 0L, '/home/log')
class login:
    home=''
    def login(self,name,passwd,lock=0):#Lock the user account, and unlock after 24hours
      self.name=name
      self.passwd=passwd
      query_u=con.query('user_info','*')
      print query_u
      if lock==True:
          a_cur=str(int(time.time()))
          con.update('user_info','lockedtime',a_cur,int(v[0]))
          return 'lock'  
      for k,v in enumerate(query_u):
        print v[1],'name','self.name',self.name
        if v[1]==self.name:
            print v[1],'name','self.name',self.name
            if int(v[3])!=0:
               print "时间差%s"%(int(time.time())-int(v[3]))
               if int(time.time())-int(v[3])<=36920:
                    return "locked"
               else:
                    con.update(user_info,lockedtime,a_cur,0)
            if v[2]!=self.passwd:
                return "passwrong"
            else:
                self.home=v[4]
                print v[4],'ggggggggggggg'
                return True
      else:
          return 'nouser'
    @classmethod                
    def admin(cls):#administrate user
      while 1:
        admin_l=['delete user','add user','modify user','unlock user']
        for i,k in enumerate(admin_l):
            print i+1,k
        what_u=raw_input('please chooser a opration:').strip()
        if what_u=='2':
            a_u=raw_input('please input username that you wanna add:').strip()
            while 1:
                a_p=raw_input('Please input passwd:').strip()
                a_c=raw_input('Please input passwd again:').strip()
                if a_p!=a_c:
                    print "the first passwd is not same as the second one,please input again!"
                    continue
                else:
                    a_h=raw_input("Please set the root directory of user:").strip()
                    m_h='/root/ftp/'+a_h
                    print m_h
                    con.new_insert('user_info','username,passwd,lockedtime,home',(a_u,a_p,0,m_h))
                    os.system('mkdir -p %s'%m_h)
                    info='''
                        New user info:
                            username:%s

                            password:%s

                            home-dir:%s
                        '''%(a_u,a_p,a_h)
                    print info
                    break
        elif what_u=='1': 
            d_u=raw_input('Please input the username that you wanna deleted:')
            a=exists(d_u)
            if a=='no':
                print "username does not exsited."
            else:    
                con.delete('user_info',"username='%s'"%d_u)
                print '%s delete sucessful.'%d_u
        elif what_u=='3':
            m_li=['modify username','modify user-homedir','modify passwd']
            for mi,mk in enumerate(m_li):
                print mi+1,mk
            what_m=raw_input('please choose a opration:').strip()
            while 1:
              what_w=raw_input('Choose to modify a user:').strip()
              what_u=exists(what_w)
              if what_m=='1':
                 if what_u=='no':
                    print " Username does not exsited, please input again"
                    continue    
                 else:
                    what_mt=raw_input('please input what you wanna modify:').strip()
                    con.update('user_info','username',what_mt,what_u)
                    print "Modify user name done!"
                    break
              elif what_m=='2':
                 if what_u=='no':
                    print "Username does not exsited"
                    continue
                 else:
                    what_mt=raw_input('please input directory you wanna modify:').strip()
                    what_ho='/var/ftp/'+what_mt
                    con.update('user_info','home',what_ho,what_u)
                    os.system('mkdir -p %s'%update)
                    print "Directoty modifed sucessfull!"
                    break
              elif what_m=='3':
                 if what_u=='no':
                    print "Username does not exsited, please input again"
                    continue
                 else:
                    what_mt=raw_input('please input password you wanna modify:').strip()
                    con.update('user_info','passwd',what_mt,what_u)
                    print "Modify passwd done!"
                    break  
              else:
                  print "chose option from (1-3), please input again！"     
                  continue  
        elif what_u=='4':
          while 1:  
            what_w=raw_input('input to unlock a user:').strip()
            what_u=exists(what_w)
            if what_u=='no':
                print "Username does not exsited, please input again"
                continue
            else:
                what_un=raw_input('Are you sure to unlock it%s?(Y/N):')
                if what_un=='Y' or what_un=='y':
                    con.update('user_info','lockedtime',0,what_u)
                    print "Unlock Done!"
                    break
                elif what_un=='N' or what_un=='n':
                    pass
def filesize(filename):
    os.system('dh -sh %s'%filename)
if __name__=='__main__':
    login.admin()
