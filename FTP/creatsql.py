#coding:utf8
import MySQLdb,os,sys
name,password=sys.argv[1],sys.argv[2]
def creat_db():#Create database
    try:
        con=MySQLdb.connect(host='localhost',user=name,passwd=password,port=3306)
        cur=con.cursor()
        sql='''
        create database ftp;
        grant all on *.* to ftp@"%" identified by "123.com";
        '''
        cur.execute(sql)
        cur.close()
        con.close()
        return 'ok'
    except MySQLdb.Error,e:
        #print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return 'no'

a=creat_db()
if a=='ok':
    os.system('mysql -u%s -p%s ftp < ./ftp.sql'%(name,password))
    print "Import data successful."
else:
    print "Fail to import data"
