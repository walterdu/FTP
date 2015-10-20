#coding:utf8
import socket,sys,time,os,getpass
import hashlib
def md5sum(filename):
    fHash = ''
    with open(filename, 'rb') as f:
        while True:
            fcont = f.read(102400000)
            if not fcont:
		new=hashlib.md5(fHash)
                return new.hexdigest()
            fpartHash = hashlib.md5(fcont)
            fHash += fpartHash.hexdigest()
try:
    host,g=sys.argv[1:3]
    port=int(g)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
except:
    print "Please input right destination address and port:eg:python client.py host port！"
    sys.exit()


print "welcome to XX ftp client!"
login=False
times=0#wrong time counter
while 1:
    name=raw_input('input your names:').strip()
    if len(name)==0:
        print "The usename cannot be empty, please input again."
        continue
    for i in xrange(4): 
        if i>=3:
            sys.exit('You account is frozen, please log in after 24 hours!')
        passwd=getpass.getpass('input your passwd:').strip()
        if len(passwd)==0:
            print "Password can not be empty, Please input again."
            continue
        userinfo='%s\t%s'%(name,passwd)
        s.sendall(userinfo)
        log_statu=s.recv(1024)
        if log_statu=='locked':
            sys.exit('You account is frozen, please log in after 24 hours!')
        elif log_statu=='passwrong':
            print "Password is wrong,input again!"
            continue
        elif log_statu=='nouser':
            print "this usr name does not exsit"
            break
        elif log_statu=='true':
            login=True 
            break

    if login==True:

        info='''
                1,put name--upload a file。
                2,get name--download file to client's folder.
                3,ls--list all the files in server
                4,del name--delete file on the server
                5,exit--client exit
                '''
        print info
        while 1:
            buf = ''
            len_data = 0
            time.sleep(0.1)
            comand=raw_input('Please input your opertation:')
            if len(comand)==0:continue
#########get###########
            s.sendall(comand)#request
            com=comand.split()[:2]
            cmd=com[0]#put or get or ls
            if cmd=='get' and len(com)==2:
                filename=comand.split()[1]#filename
                str_len=s.recv(1024)
                if str_len=='no':
                    print "Did not find file% or size is null."%filename
                    continue
                print str_len
                while 1:
                    str_tmp = s.recv(819600)
                    if not len_data:
                        ofh=open(filename, 'wb+')
                        ofh.close()   
                        len_data=int(str_len)
                    ofh=open(filename, 'ab+')
                    ofh.writelines(str_tmp)
                    ofh.close()   
                    bufsize=os.path.getsize(filename)
                    len_statu=100 * bufsize/len_data
                    print 'recv ratio:'+str(len_statu)+'%'
                    if bufsize==len_data:
                        s.send('aaaa')
                        print 'Verifyiing MD5 Hold on.....'
                        get_md5=s.recv(1024)
                        locmd5=md5sum(filename)
                        if locmd5==get_md5:
                            print "Transmission finished!server: %s  client:%s"%(get_md5,locmd5)
                            break
                        else:
                            print "the file is not completely!..."
                            break
                    
            elif cmd=='put' and len(com)==2:
                time.sleep(0.06)
                filename=comand.split()[1]
                size=os.path.getsize(filename)
                print "the size of file%s"%size
                with open(filename,'rb') as f:
                    while 1:
                        a=f.read(819600)
                        s.sendall(a)
                        f_size=s.recv(1024)
                        print 'recv ratio %s' % str(100 * int(f_size)/size)+'%'
                        if (100 * int(f_size)/size)==100:
                            print " Verifyiing the integraty of the file....Hold on..."
                            s.sendall('ok')    
                            ggg=s.recv(1024)
                            s.sendall(md5sum(filename))
                            get_p=s.recv(1024)#
                            if get_p=='ok':
                                print "File transmission successfull..."
                            else:
                                print "File transmission fail ...!"
                            break
                        
            elif cmd=='del' and len(com)==2:
                p=s.recv(1024)
                print p
            elif cmd=='exit':
                sys.exit()
            elif cmd=='ls':
                time.sleep(0.02)
                tmp1=s.recv(1024)
                print tmp1
            else:
                tmp1=s.recv(1024)
                print tmp1
                print "Please input the operation again..."
                continue
    else:continue            
#print 'congratulations, your file %s has been received successfully, file len%s' % (fn, len_data)
