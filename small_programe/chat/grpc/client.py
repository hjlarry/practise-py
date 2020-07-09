import threading
import tkinter
import tkinter.simpledialog

import grpc

from proto import chat_pb2
from proto import chat_pb2_grpc


class Client:
    def __init__(self, username, window):
        self.window = window
        self.username = username
        channel = grpc.insecure_channel("localhost:11912")
        self.conn = chat_pb2_grpc.ChatServerStub(channel)

    def _listent_for_messages(self):
        for note in self.conn.ChatStream(chat_pb2.Empty()):
            self.chat_list.insert(tkinter.END, f"[{note.name}] {note.message} \n")

    def _setup_ui(self):
        self.chat_list = tkinter.Text()
        self.chat_list.pack(side=tkinter.TOP)
        self.lbl_username = tkinter.Label(self.window, text=self.username)
        self.lbl_username.pack(side=tkinter.LEFT)
        self.entry_message = tkinter.Entry(self.window, bd=5)
        self.entry_message.bind("<Return>", self.send_message)
        self.entry_message.focus()
        self.entry_message.pack(side=tkinter.BOTTOM)

    def send_message(self, event):
        message = self.entry_message.get()
        if message:
            n = chat_pb2.Note()
            n.name = self.username
            n.message = message
            self.conn.SendNote(n)

    def run(self):
        threading.Thread(target=self._listent_for_messages, daemon=True).start()
        self._setup_ui()
        self.window.mainloop()


if __name__ == "__main__":
    root = tkinter.Tk()
    frame = tkinter.Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()
    username = None
    while username is None:
        username = tkinter.simpledialog.askstring(
            "Username", "What`s your username?", parent=root
        )
    root.deiconify()
    c = Client(username, frame)
    c.run()

