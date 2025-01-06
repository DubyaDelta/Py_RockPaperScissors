import socket
import threading
from tkinter import *

# Initialize global variables
client_socket = None
root = Tk()

# Function to connect to the server
def connect_to_server():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5555))  # Change IP for external server
    threading.Thread(target=receive_result).start()

# Function to receive the game result from the server
def receive_result():
    while True:
        try:
            result = client_socket.recv(1024).decode()
            l4.config(text=result)
        except:
            print("Disconnected from server.")
            break

# Send the player's choice to the server
def send_choice(choice):
    client_socket.send(choice.encode())
    button_disable()

# Button actions
def isrock():
    send_choice("Rock")

def ispaper():
    send_choice("Paper")

def isscissor():
    send_choice("Scissors")

# GUI setup
root.geometry("300x300")
root.title("Rock Paper Scissor Game")

Label(root, text="Rock Paper Scissor", font="normal 20 bold", fg="blue").pack(pady=20)

frame = Frame(root)
frame.pack()

l1 = Label(frame, text="Player", font=10)
l2 = Label(frame, text="VS", font="normal 10 bold")
l3 = Label(frame, text="Computer", font=10)

l1.pack(side=LEFT)
l2.pack(side=LEFT)
l3.pack()

l4 = Label(root, text="", font="normal 20 bold", bg="white", width=15, borderwidth=2, relief="solid")
l4.pack(pady=20)

frame1 = Frame(root)
frame1.pack()

b1 = Button(frame1, text="Rock", font=10, width=7, command=isrock)
b2 = Button(frame1, text="Paper", font=10, width=7, command=ispaper)
b3 = Button(frame1, text="Scissors", font=10, width=7, command=isscissor)

b1.pack(side=LEFT, padx=10)
b2.pack(side=LEFT, padx=10)
b3.pack(padx=10)

def button_disable():
    b1["state"] = "disable"
    b2["state"] = "disable"
    b3["state"] = "disable"

connect_to_server()
root.mainloop()
