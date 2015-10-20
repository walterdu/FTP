# Please run this program server.py and client.py with root
1. First import the database.
 	Library name: ftp
 	Username: ftp
 	Password: 123.com
 	Manual Import: 1.create database ftp; 2.use ftp 3.source ./ftp.sql --- [path as appropriate]
 Auto-import (only local or virtual machine): first ftp.sql in the same directory and creatsql
 Executive: python creatsql.py root passwd (native root user and password)
Note: The user's home directory is: / root / ftp / username Upload delete files in this directory can be viewed

2.manager: python config.py: offers four options CRUD user information also unlock feature, users will be unlocked.
        
3.server: python server.py port (port means the current use of the port number)

4.client: python client localhost port (localhost refers to the address of the server end of the connection port refers to the port number)


client-side many landing may have put, get, ls, del function respectively (a.put filename: upload a file to the user's home directory.
                                                b.get filename: downloaded from the home directory of the current folder
                                                c.ls: View home directory file
                                                d.del filename: delete a file home directory) filename refers to the filename
                                                                                                        
Tested: You can upload large files of data (2G above) and to verify file integrity
Use hashlib module. Blocking the way to read the file hash. To verify the integrity of the file data.


User login: verify that the user has not re-enter, after a successful landing, in the user's home directory upload and download files.
Password can not be blank, enter the three locks, 24 hours automatically unlock, manually unlock: python config.py have unlocked option
