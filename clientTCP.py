import threading
import socket
alias = input('Enter your alias :) >>  ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59000))


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            elif message == "send":
                pass
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        try:
            message = input("")
            if message == "list!":
                client.send("list!".encode('utf-8'))
            elif message == "help!":
                print("\n_______________________________________________________________________________________\n"
                      "\n\t <<<<<< {{{ Warning }}} >>>>>> it must enter your Special ID :) \n"
                      "\n\t Write : {help!} : To print help list\n"
                      "\n\t Write : {list!} : To print list of IDs\n"
                      "\n\t Write : {(id receive)>>message} : To send message to one ID (point to point)\n"
                      "\n\t Write : {add! (id number) (id number) .. } To creat Groub\n"
                      "\n\t Write : {STG> message} To send in Groub\n"
                      "\n\t Write : {(id receive)@(the path of the file)}\n"
                      "\n\t Write : {logout} to exit client from server\n"
                      "\n_____________________________________________________________________________________\n"
                      )
            elif message == "logout":
                client.close()
                break

            else:
                client.send(message.encode('utf-8'))
        except:
            print("Error")



receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
