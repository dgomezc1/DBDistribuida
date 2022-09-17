# ********************************************************************************************
    # Proyecto 1
    # Course: ST0263 - Topicos Especiales de Telemática
    # Implementacion base de datos minimalista
    #Pascual Gomez Londoño
    #David Gomez Correa
    #Sebastian Granda Gallego
# ********************************************************************************************

# Import libraries for networking communication and concurrency...

import socket
import constants

def validador(h):       #Hay que actualizarlo con expresiones regulares
    return True

def main(direccion, port):
    try: 
        command_to_send = ""
        while command_to_send != constants.QUIT :                                       #Mientras que el comando ingresado por el usuario sea diferentes de QUIT
            command_to_send = input("DB>>")                                             #Pedimos por consola el comando a ingresar
            client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)            #Inicializamos el socket    
            if validador(command_to_send) and command_to_send != constants.QUIT:        #Validamos que el comando no sea QUIT y que sea valido
                client_socket.connect((direccion,port))                                 #Nos conectamos a la base de datos por direccion y puerto                   
                client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))   #Se codifica el mensaje y se envia
                data_received = client_socket.recv(10000000)                            #Recibimos la informacion que llega del servidor
                print(data_received.decode("utf-8"))                                    #Imprimimos el mensaje de respuesta decodificado                            
                client_socket.close()                                                   #Cerramos la conexion con la base de datos                               
            elif command_to_send == constants.QUIT:
                break                                                                   #Salimos del ciclo en caso de que el usuario ingrese QUIT
            else:       
                print('Please enter a valid command')                                   #En caso de ingresar un comando invalido
            #client_socket.connect((direccion,port, host_send))  
    except Exception as e:                                                              #Excepcion en caso de ocurrir un error
        print(e)
        print('Error, please try again...')

    print('Closing connection...BYE BYE...')                                            #Final del programa
   

if __name__ == '__main__':
    print('***********************************')            #Inicio del programa
    print('Client is running...')
    direccion = input('Enter the IP Address: ')             #Se le pide por pantalla al usuario direccion y puerto
    port = int(input('Enter the Port: '))
    print('***********************************') 
    print('\nEnter \"QUIT\" to exit')                       #Impresion de comandos disponibles en la base de datos
    print('Input commands:')
    print('QUIT, GET, SET, UPDATE, DELETE\n')               #Llamamos la funcion main con la direccion y el puerto
    main(direccion, port)