import socket
from _thread import *
import pickle
from game import Game

server = "192.168.0.18"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
game = Game()
playerCount = 0

def threaded_client(conn, player_num):
    global playerCount
    player_info = game.createPlayer(player_num)
    conn.send(str.encode(str(player_info)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            if not data:
                break
            else:
                if data == 'get':
                    pass
                    #player_data = game.get_player_info(player_num)
                    #conn.sendall(pickle.dumps(player_data))
                #if data == value? of the bet maybe 
                #maybe have a method of data that retrieves all of the pertinent information and sends it to the player
                #conn.sendall(pickle.dumps(game))
        except:
            break
    print("Lost connection")
    game.create_computer(player_num)
    conn.close()

while True:
    conn, addr = s.accept() #conn = IP address, port/id 
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, playerCount))
    playerCount += 1