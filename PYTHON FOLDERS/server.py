import socket
import threading

HOST = '192.168.0.144'
PORT = 9090


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
	for client in clients:
		client.send(message)

def extractnic(message):
	msg = message.decode('utf-8')
	b = msg.find("/to/")
	a= msg.find("//")
	print(f"a = {a}")
	nic = msg[b+4:a]
	return nic

def handle(client):
	while True:
		try:
			message = client.recv(1024)
			print(f"{nicknames[clients.index(client)]} :: {message}")
			if "/to/" in message.decode('utf-8'):

				nic = extractnic(message)
				nickc = bytes(nic, 'utf-8')

				if nickc in nicknames :
					wclient=clients[nicknames.index(nickc)]

					wclient.send(message)
					client.send(message)

				else:
					print(f"nope")
					broadcast(message)

			else:
				broadcast(message)

		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			nicknames.remove(nickname)
			break

def receive():
	while True:
		client, address = server.accept()
		print(f"Connected with {str(address)} ! ")

		client.send("NICK".encode('utf-8'))
		nickname = client.recv(1024)

		nicknames.append(nickname)
		clients.append(client)

		print(f"nickname of the client is {nickname}")
		broadcast(f"{nickname} is now connected to the server !\n".encode('utf-8'))
		client.send("Conected to the server".encode('utf-8'))

		thread = threading.Thread(target=handle, args = (client,))
		thread.start()

print("Server running")
receive()



