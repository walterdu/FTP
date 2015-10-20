#coding:utf8
import SocketServer,sys,commands,time,os
import hashlib,config
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
class FtpHandler(SocketServer.BaseRequestHandler):
    def handle(self):
      i=0  
      while 1:
        login=config.login()  
        loginfo = self.request.recv(1024).strip().split('\t')[:2]
        user=loginfo[0]
        passwd=loginfo[1]
        log_statu=login.login(user,passwd)
        if i>=2:
            u_id=config.exists(user)
            config.con.update('user_info','lockedtime',int(time.time()),u_id)
	    break
        i+=1
        if log_statu=='passwrong':
            self.request.sendall('passwrong')
        elif log_statu=='nouser':
            self.request.sendall('nouser')
        elif log_statu=='locked':
            self.request.sendall('locked')
        elif log_statu==True:
            home_dir=login.home
            if os.path.exists(home_dir)==False:
                os.system('mkdir -p %s'%home_dir)
            self.request.sendall('true')
            while 1:
                print "Waiting command----------"
                get_data = self.request.recv(1024).strip().split()
                print get_data,'paraeter from client'
                if len(get_data)>=2:
                    cmd, filename = get_data[:2]
                    target_file='%s/%s'%(home_dir,filename)
                    if cmd == 'get':
                        len_buf=0
                        if os.path.exists(target_file)==True and os.path.getsize(target_file)!=0:
                            size=os.path.getsize(target_file)
                            print 'Sending size%s file'%size
                            self.request.send(str(size))
                            time.sleep(0.05)
                            with open(target_file,'rb')as f:
                                while 1:
                                    #if not f.readline():break
                                    a=f.read(819600)#read 16392byte once time
                                    if len(a)==0:
                                        g=self.request.recv(1024)
                                        self.request.sendall(md5sum(target_file))   
                                        break
                                    else:    
                                        self.request.sendall(a)
                                        
                        else:
                             self.request.sendall('no')
                    elif cmd == 'put':
                        len_data=0
                        while 1:
                            str_tmp = self.request.recv(819600)
                            if str_tmp=='ok':
                                self.request.sendall('down')
                                get_md5=self.request.recv(1024)#recieve client MD5
                                locmd5=md5sum(target_file)
                                print "server:%s  client:%s"%(locmd5,get_md5)
                                if locmd5==get_md5:
                                    self.request.sendall('ok')
                                else:
                                    self.request.sendall('no')
                                break
                            if not len_data:
                                ofh=open(target_file, 'wb+')
                                ofh.writelines(str_tmp)
                                len_data=1
                                ofh.close()
				size=os.path.getsize(target_file)
                                self.request.send(str(size))
                            else:    
                                ofh=open(target_file, 'ab+')
                                ofh.writelines(str_tmp)
                                ofh.close()
                                size=os.path.getsize(target_file)
                                self.request.send(str(size))
                                
                    elif cmd == 'del':
                        statu=commands.getstatusoutput('rm -rf %s'%target_file)
                        if statu[0]==0:
                            self.request.sendall('Delete%sSuccess'%get_data[1])
                        else:
                            self.request.sendall("Wrong Operration")
                    else:
                        statu=commands.getstatusoutput(get_data[0])
                        if statu[0]==0:
                            self.request.sendall(statu[1])
                        else:
                            self.request.sendall("Wrong Operration")
                elif len(get_data)<2:
                    print '%s %s'%(get_data[0],home_dir)
                    statu=commands.getstatusoutput('%s %s'%(get_data[0],home_dir))
                    if statu[0]==0 and len(statu[1])!=0:
                        self.request.sendall(statu[1])
                        print statu[1],'Command excute successfull.'
                        continue
                    elif len(statu[1])==0:
                        self.request.sendall("NUll") 
                    else:
                        self.request.sendall("false")
                        print 'Command excute fail.'
                        continue
if __name__=='__main__':
    g=sys.argv[1]
    host,port = 'localhost',int(g)
    server = SocketServer.ThreadingTCPServer((host,port),FtpHandler)
    server.allow_reuse_address = True#detecting
    server.serve_forever() 


