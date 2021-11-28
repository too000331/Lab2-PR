import socket
import threading
import ftplib
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 8080
HOSTNAME = "ftp.dlptest.com"
USERNAME = "dlpuser"
PASSWORD = "rNrKYTX9g7z3RgJRmxWuGHbeu"



class Client:

    def __init__(self, host, port, hostname, user, pasw):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.ftp_server = ftplib.FTP(hostname, user, pasw)  # connect FTP server
        self.ftp_server.encoding = "utf-8"   # force UTF-8 encoding

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Enter your nickname", parent=msg)

        self.gui_done = False
        self.running = True

        receive_thread = threading.Thread(target=self.receive)

        receive_thread.start()
        self.gui_loop()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title('Chatroom')
        self.win.configure(bg="lightyellow")

        self.chat_label = tkinter.Label(self.win, text="Chat", bg="lightyellow")
        self.chat_label.config(font=("Calibri", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message", bg="lightyellow")
        self.msg_label.config(font=("Calibri", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Calibri", 12))
        self.send_button.pack(padx=20, pady=5)



        self.gui_done = True

        self.win.protocol("WH_DELETE_WINDOW", self.stop)
        self.win.mainloop()



    def send_message(self, message):
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.send_message(message)

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))

                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        print(message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disable')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break



client = Client(HOST, PORT, HOSTNAME, USERNAME, PASSWORD)
