# ********************************************************************************************
    # Proyecto 1
    # Course: ST0263 - Topicos Especiales de Telemática
    # Implementacion base de datos minimalista
    #Pascual Gomez Londoño
    #David Gomez Correa
    #Sebastian Granda Gallego
# ********************************************************************************************

from email.mime import base
from database import Databases
import socket
import configuracion
import hashlib

# Defining a socket object...
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)           #AF_INET define el tipo de direccion (ipv4), y modo TCP
server_address = configuracion.direccion                                   #Define la direccion del servidor
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        #Configuracion del socket
puerto = int(input("Ingrese un puerto: "))
nomArchivo = ".\\"+str(puerto)
baseDeDatos = Databases(nomArchivo)                                              #Inicilizamos la base de datos

def main():
    print("\n***********************************")            #Imprimimos datos relevantes de la ejecucion
    print("Server is running...")
    print("Dir IP:", server_address)
    print("Port:", puerto)
    server_execution()                                        #Se llama a  la funcoin server_execution para iniciar la ejecucion

def hash_table(clave):
    result = result = (hashlib.sha1(clave.encode()))
    hexa = result.hexdigest()
    return hexa

def manejador(client_connection, client_address):
    print(f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}')  #Imprimimos de donde viebne la conexion
    data_recevived = client_connection.recv(configuracion.RECV_BUFFER_SIZE)                     #Guardamos los datos entrantes por el buffer de conexion            
    command  = str(data_recevived.decode(configuracion.ENCONDING_FORMAT))                       #Decodificamos el comando
    print(command)                                              #Imprimimos el comando entrante
    command = command.split()                                   #Dividimos el comando por espacios
    operacion = command[0]                                      #Tomamos la primera posicion donde se encuentra la operacion CRUD a realizar
    if(operacion==configuracion.GET):                           #En caso de que la operacion sea GET
        print("get")
        clave = hash_table(command[1])
        response  = baseDeDatos.get(clave)                      #Llamamos la funcion de get de nuestro objeto de baseDeDatos con la key
        client_connection.sendall(response)                     #Enviamos el mensaje de repuesta
    elif(operacion==configuracion.SET):                         #En caso de que la operacion sea SET
        print("set")
        clave = hash_table(command[1])
        response  = baseDeDatos.save(clave, command[2])         #Llamamos la funcion de SET del objeto baseDeDatos con la key y el valor
        client_connection.sendall(response)                     #Enviamos el mensaje de repuesta
    elif(operacion==configuracion.UPDATE):                      #En caso de que la operacion sea UPDATE
        print("update")
        clave = hash_table(command[1])
        response  = baseDeDatos.save(clave, command[2])         #Llamamos la funcion de UPDATE del objeto baseDeDatos con la key y el valor
        client_connection.sendall(response)                     #Enviamos el mensaje de repuesta
    elif(command[0]==configuracion.PING):
        response = "PONG".encode("utf-8")
        client_connection.sendall(response)
    else:    
        clave = hash_table(command[1])                          #Por ultimo en caso de que la operacion se DELETE   
        response  = baseDeDatos.delete(clave)                   #Llamamos la funcion de DELETE de nuestro objeto de baseDeDatos con la key
        client_connection.sendall(response)                     #Enviamos el mensaje de repuesta
    print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...\n')      
    client_connection.close()                                   #Cerramos la conexion con el cliente

def server_execution():
    tuple_connection = (server_address, puerto)                         #Se crea una dupla con la direcion y el puerto del servidor    
    server_socket.bind(tuple_connection)                                #Se abre el socket con los valores anteriores                  
    print ('Socket is bind to address and port...')
    server_socket.listen(5)                                             #Se define una cola de 5 posicione para alamacenar los datos entrantes                                           
    print('Socket is listening...')
    while True:                                                         #Bucle infinito para recibir los datos por el buffer
        client_connection, client_address = server_socket.accept()      #En caso de que llegue una conexion guardamos la conecion y la direccion del cliente
        manejador(client_connection, client_address)                    #Llamamos a la funcion manejador y mandamos los datos anteriores


    print('Socket is closed...')
    server_socket.close()


if __name__ == "__main__":
    main()
