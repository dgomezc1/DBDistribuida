# ********************************************************************************************
    # Proyecto 1
    # Course: ST0263 - Topicos Especiales de Telemática
    # Implementacion base de datos minimalista
    #Pascual Gomez Londoño
    #David Gomez Correa
    #Sebastian Granda Gallego
# ********************************************************************************************

import os,json 

class Databases: 

    def __init__(self , location=".\\db"):                      
        self.location = os.path.expanduser(location)        #Se busca ek archivo de db en el directorio
        self.loaddb(self.location)                          #Se llama a la funcion cargar base de datos 

    def loaddb(self, key): 
        self.db = json.load(open(self.location, "r")) if os.path.exists(self.location) else {}  #Se carga el archivo de json en modo lectura
        return True                                                                             #Si no hay errores se retorna true

    def savedb(self):                   
        try: 
            json.dump(self.db , open(self.location, "w+"))          #Se trata de escribir el json en el archivo db
            return True                                             #En caso de lograrlo se retorna True
        except: 
            return False                                            #False en caso de no lograr escribir el archivo en local

    def save(self, key, value): 
        try: 
            self.db[str(key)] = value                                           #Se toma el json y a la clave que se ingresa se le asigna el value
            self.savedb()                                                       #Se llama a la funcion savedb para guardar los cambios en local
            return "Base de datos actualizada".encode("utf-8")                  #Se retorna mensaje de confirmacion
        except Exception as e: 
            print("[X] Error Saving Values to Database : " + str(e))            #En caso de error, se imprime el error
        return "No se ha podido actualizar la base de datos".encode("utf-8")    #Se retorna el mensaje de error   

    def get(self , key): 
        try: 
            return self.db[key].encode("utf-8")                                 #Retornamos el valor  asociado a la clave
        except KeyError:  
            return "400 Elemento no encontrado".encode("utf-8")                 #Se retorna mensaje de error en caso de no encontrar el archivo

    def delete(self , key): 
        if not key in self.db:                                              #Preguntamos si la clave existe en la base de datos
            return "400 Elemento no encontrado".encode("utf-8")             #En caso de no existir se envia mensaje de erro
        del self.db[key]                                                    #En caso de que exista la clave, se elimina esta
        self.savedb()                                                       #Se guarda el cambio de datos en local
        return "200 OK Elemento eliminado con exito".encode("utf-8")        #Se retorna el mensaje de confirmacion

    def resetdb(self):              
        self.db={}              #Resetamos el objecto de json
        self.savedb()           #Se guardan los cambios en local
        return True 

