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
    player= game.createPlayer(player_num)
    
    try:
        
        #conn.sendall(pickle.dumps(player)) #consider passing just the player number and then updating from there. Is there really antything that 
                                           # the data class does to the player classes that aren't within a function call? 
        conn.send(str.encode(str(player_num)))
        print("sending data...")
    except socket.error as e:
        print(e)
        print("could not send data")
    reply = ""
    while True:
        print("in the while loop")
        try:
            print("receiving data...")
            data = conn.recv(4096).decode() 
            if not data:
                print("No data to receive")
                break
            else:
                print("We found data")
                print(data)
                if data == 'get':
                    
                    #player_data = game.get_player_info(player_num)
                    #conn.sendall(pickle.dumps(player_data))
                #if data == value? of the bet maybe 
                #maybe have a method of data that retrieves all of the pertinent information and sends it to the player
                #conn.sendall(pickle.dumps(game))
        except:
            print("could not receive the data")
            break
    print("Lost connection")
    game.create_computer(player_num)
    conn.close()

while True:
    conn, addr = s.accept() #conn = IP address, port/id 
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, playerCount))
    playerCount += 1