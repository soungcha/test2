#!/usr/bin/env python
 #-*- coding: utf-8 -*-

from ftplib import FTP
import sys,getpass,os.path

host = '115.28.179.60'
username ='imgftp'
password = 'imgftp'

localfile ='d:\\temp\\wh3.jpg'
remotepath ='./linkedin/'
print "HELLO"
f =FTP(host)
f.login(username,password)
print "Welcome:",f.getwelcome()
f.cwd(remotepath)
fd = open(localfile,'rb')
f.storbinary('STOR %s' % os.path.basename(localfile),fd)
fd.close()

f.quit()

# if __name__ == "__main__":
#     Main()



