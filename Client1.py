# import all the required modules
import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
# from chat import *

PORT = 5000
SERVER = "192.168.0.153"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

# Creating a new client socket and connect to the server
client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
client.connect(ADDRESS)


# GUI class for the chat
class CampCo:
    # constructor method
    def __init__(self):

        # chat window
        self.Window = Tk()
        self.Window.iconbitmap("E:\Ammar work\CAMCom\icon.ico")
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.iconbitmap("E:\Ammar work\CAMCom\icon.ico")
        self.bg = PhotoImage(file='E:\Ammar work\CAMCom\Logo.png')
        self.l = Label(self.login, image=self.bg)
        self.l.place(x=0, y=0, relwidth=1, relheight=1)
        # self.l.after(3000, self.l.destroy)

        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.geometry("587x480+400+100")

        def clear_login(event):
            self.entryName.delete(0, END)

        self.entryName = Entry(self.login,
                               font="Helvetica 14")
        self.entryName.insert(0, "Name")
        self.entryName.bind("<Button-1>", clear_login)

        self.entryName.place(relwidth=0.4,
                             relheight=0.08,
                             relx=0.25,
                             rely=0.7)

        self.entryName.focus()

        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold", bg="#008080",
                         command=lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx=0.68,
                      rely=0.7)

        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)

        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    # The main layout of the chat
    def layout(self, name):

        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CampCo")

        self.Window.geometry("500x600+450+50")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(bg="#02D6D9")
        self.labelHead = Label(self.Window,
                               bg="#008080",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#02D6D9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=10,
                             bg="#008080",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#02D6D9",
                                 height=50)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#018788",
                              fg="#EAECEE",
                              font="Georgia 18")

        self.entryMsg.place(relwidth=0.74,
                            relheight=0.07,
                            rely=0.035,
                            relx=0.011)

        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#018788",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.035,
                             relheight=0.07,
                             relwidth=0.22)

        self.textCons.config(cursor="arrow")
        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, message + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                print("An error occured!")
                client.close()
                break

    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:

            message = f"{self.name}: {self.msg}"
            client.send(message.encode(FORMAT))
            break


p = CampCo()
