import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
import os


def extrctp(message):
	a =message.find("//")
	b=message.find("\n")
	path = message[a+3:b-1]
	return path

class Client(object):
	
	def __init__(self, host, port):

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((host, port))

		msg = tkinter.Tk()
		msg.withdraw()

		self.nickname = simpledialog.askstring("Nickname ", "Please choose a nickname", parent=msg)

		self.gui_done = False
		self.running = True

		gui_thread = threading.Thread(target=self.gui_loop)
		receive_thread = threading.Thread(target=self.receive)

		gui_thread.start()
		receive_thread.start()

	def gui_loop(self):
		self.win = tkinter.Tk()
		self.win.configure(bg="Dim gray")

		self.chat_label = tkinter.Label(self.win, text="BERSERKER: connected as "+self.nickname, bg="Dim gray", fg="White")
		self.chat_label.config(font = ("Arial", 12))
		self.chat_label.pack()

		self.text_area = tkinter.scrolledtext.ScrolledText(self.win, bg="gray")
		self.text_area.pack(padx=20, pady=5)
		self.text_area.config(state='disabled')

		self.msg_label = tkinter.Label(self.win, text="Message : ", bg="Dim gray", fg="White")
		self.msg_label.config(font = ("Arial", 12))
		self.msg_label.pack()

		self.input_area = tkinter.Text(self.win,  bg="gray", height=3)
		self.input_area.pack(padx=20, pady=5)

		self.send_button=tkinter.Button(self.win, text="Send", bg="Dim gray", fg="White", command = self.write)
		self.send_button.config(font = ("Arial", 12))
		self.send_button.pack(padx=20, pady=5)

		self.gui_done=True


		self.win.protocol("WM_DELETE_WINDOW", self.stop)


		self.win.mainloop()

	

	def write(self):
		message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"

		
		if "/file/" in message :
			if "//" in message :
				pathb = extrctp(message)
				print(f"path = {pathb}")
				with open(pathb, 'rb') as file:
					while True:
						data = file.read(1024)
						if not data:
							break
						self.sock.send(message.encode('utf-8') + data)
						self.input_area.delete('1.0', 'end')
		else:
			self.sock.send(message.encode('utf-8'))
			self.input_area.delete('1.0', 'end')





	def stop(self):
		self.running = False
		self.win.destroy()
		self.sock.close()
		exit(0)

	def receive(self):
		while self.running:
			try:
				message = self.sock.recv(1024).decode('utf-8')
				if message == "NICK":
					self.sock.send(self.nickname.encode('utf-8'))
				else:
					if self.gui_done:
						self.text_area.config(state='normal')
						self.text_area.insert('end', message)
						self.text_area.yview('end')
						self.text_area.config(state='disabled')
			except ConnectionAbortedError:
				break
			except:
				print('Error')
				self.sock.close()
				break	


def main():
	ip = tkinter.Tk()
	ip.withdraw()
	HOST = simpledialog.askstring("ip ", "server address", parent=ip)
	PORT = simpledialog.askstring("Port ", "Port number", parent=ip)
	client = Client(HOST, int(PORT))
		

main()