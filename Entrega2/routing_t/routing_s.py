from msilib.schema import Directory
import os
import socket

class Routing_Severs:
    def __init__(self, location=".\\conf"):
        self.location = os.path.expanduser(location)
        archivo = open(self.location, "r")
        lista = archivo.readlines()
        prim_linea = lista[0].split()
        n = int(prim_linea[2])
        self.direcciones = []
        for i in range(1,n+1):
            datos = lista[i].split(":")
            dato = (datos[0], int(datos[1]))
            self.direcciones.append(dato)
        print(self.direcciones)
        self.aprovacion = self.verificacion_nodos()
    
    def verificacion_nodos(self):
        for i in self.direcciones:
            client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client_socket.connect(i)
            command_to_send = "PING "
            client_socket.send(bytes(command_to_send,"utf-8"))
            data_received = client_socket.recv(10000000).decode("utf-8")
            if data_received != "PONG":
                client_socket.close()  
                return False
            client_socket.close()  
        return True
        
m = Routing_Severs()
print(m.aprovacion)