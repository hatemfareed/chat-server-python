
import threading
import socket
# host = '127.0.0.1'
# port = 59000
host = '127.0.0.1'
port = 80
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []
ID = []
group = []


def broadcast(message):
    for client in clients:
        client.send(message.encode("utf-8"))

def listClients(client): #list!
    try:
        index = 0
        client.send("\n_______________________________________________________________________________________\n".encode("utf-8"))
        client.send("\naliases\t:\tID\n".encode("utf-8"))
        for a in aliases:
            id = ID[index]
            message ='\n' + a + '\t:\t' + id + '\n'
            client.send(message.encode('utf-8'))
            index = index + 1
        client.send("\n_______________________________________________________________________________________\n".encode("utf-8"))
    except:
        return

def  checkIdInGroup(client):
    try:
        for c in group:
            if client == c:
                return True
        return False
    except:
        print("Error")

def STG(message,client):
    try:
        index = clients.index(client)
        alias = aliases[index]
        cmd = message.split(">")
        message = f'{alias} :' + f'{cmd[~0]}'
        for g in group:
            g.send(message.encode("utf-8"))
    except:
        print("Error")

def addGroup(message,client):   # add! 11 22 33
    idGroup = message.split(' ')
    group.append(client)
    index = 0
    try:
        for s in idGroup:
            if index == 0:
                index = index +1
                client.send("gg:) you are in group".encode("utf-8")) # the client who create the group
            else:
                i = ID.index(s)
                group.append(clients[i])
                clients[i].send("gg:) you are in group".encode("utf-8"))

    except:
        client.send("the id which was select is not Existing , Please return".encode("utf-8"))
        return

def sendTofriend(message,client):
    try:
        list = message.split(">>")
        id = list[0]
        message = list[~0]
        i = ID.index(id)
        index = clients.index(client)
        alias = aliases[index]
        message = f'{alias} :' + f' {message} '
        clients[i].send(message.encode("utf-8"))
    except:
        print("Error")

def sendfile(message,client):
    try:
        list =message.split("@")
        receiver = list[0]
        path = list[1]
        i = ID.index(receiver)
        index = clients.index(client)
        alias = aliases[index]

        f = open(f'{path}', "r")
        readFile = f.read()
        message = f'{alias} \n/*' + f' {readFile} */'
        print(message)
        clients[i].send(message.encode("utf-8"))
    except:
        print("Error path")


# Function to handle clients'connections
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
            if ">>" in message:
                sendTofriend(message,client)

            elif message == 'list!':
                listClients(client)
            elif "@" in message:  #send file
                sendfile(message,client)
            elif "add!" in message :
                addGroup(message,client)
            elif "STG" in message:
                isInGroup = checkIdInGroup(client)
                if isInGroup:
                    STG(message,client)
                else:
                    client.send("you are not in group !!:(".encode("utf-8"))
            else:
                index = clients.index(client)
                alias = aliases[index]
                message = f'{alias} :' + f' {message} '
                broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!')
            aliases.remove(alias)
            break
# Main function to receive the clients connection

def validId(id) :
    for i in ID:
        if i == id:
            return False
    return True


def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode("utf-8")
        client.send("Enter Your ID: ".encode('utf-8'))
        id =  client.recv(1024).decode("utf-8")
        isValidId =  validId(id)
        if isValidId:
            ID.append(id)
            aliases.append(alias)
            clients.append(client)
            print(f'The alias of this client is {alias}'.encode('utf-8'))
            broadcast(f'{alias} has connected to the chat room')
            client.send('you are now connected! press help!'.encode('utf-8'))
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
        else:
            while(isValidId == False ):
                client.send("you connect with used id :(".encode("utf-8"))
                client.send("Enter Your ID: ".encode('utf-8'))
                id2 = client.recv(1024).decode("utf-8")
                isValidId = validId(id2)
                if isValidId:
                    ID.append(id2)
                    aliases.append(alias)
                    clients.append(client)
                    print(f'The alias of this client is {alias}'.encode('utf-8'))
                    broadcast(f'{alias} has connected to the chat room')
                    client.send('you are now connected! press help!'.encode('utf-8'))
                    # broadcast(f'{aliases}'.encode())
                    thread = threading.Thread(target=handle_client, args=(client,))
                    thread.start()

receive()
