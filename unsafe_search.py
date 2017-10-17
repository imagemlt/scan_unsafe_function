#coding=utf-8

import threading
import os
import sys
import signal


sys.setrecursionlimit(1000000)
funclist=[]
threadpool=[]
mutex = threading.Lock()
logfile=None

def quit(signum, frame):
    print 'You choose to stop me.'
    sys.exit(1)

def scanfile(filename):
	global logfile
	mutex.acquire()
	print "[+]start scan "+filename
	mutex.release()
	f=open(filename,"r")
	i=1
	for line in f:
		for func in funclist:
			if func in line:
				mutex.acquire()
				print "[+]%s,line %d,unsafe function [%s]"%(filename,i,func)
				if logfile is not None:
					logfile.write("[+]%s,line %d,unsafe function [%s]\n"%(filename,i,func))
				mutex.release()
		i=i+1
	f.close
	
def generate_list():
	global funclist
	try:
		f=open("funclist.txt","r")
		funclist=[x.rstrip("\n") for x in f]
	except IOError as err:
		print 'File Error:'+str(err)
		sys.exit(0)

def scandir(direct):
	global threadpool
	if os.path.isfile(direct):
			t=threading.Thread(target=scanfile,args=(direct,))
			t.start()
			threadpool.append(t)
	elif os.path.isdir(direct):
			for i in os.listdir(direct):
				scandir(direct+"/"+i)

def main():
	global logfile
	if len(sys.argv)<2:
		print "Usage: %s [--log] [directory]" % sys.argv[0]
		sys.exit(0)
	for i in sys.argv:
		if i=="--log":
			logfile=open("scan_for_"+sys.argv[-1].encode('hex')+".txt","w")
	if not os.path.exists(sys.argv[-1]):
		print "Directory %s not found!" % sys.argv[-1]
		sys.exit(0)
	generate_list()
	scandir(sys.argv[-1])
	if len(threadpool)>0:
		for t in threadpool:
			t.join()
	if logfile is not None:
		print "logged to scan_for_"+sys.argv[-1]+".txt"
		logfile.close()
	
if __name__=='__main__':
	main()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
