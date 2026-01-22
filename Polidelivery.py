import os
import heapq
from collections import deque

def validar_contrasena(contrasena):
    tiene_minuscula = any(c.islower() for c in contrasena)
    tiene_mayuscula = any(c.isupper() for c in contrasena)
    tiene_numero = any(c.isdigit() for c in contrasena)
    return tiene_minuscula and tiene_mayuscula and tiene_numero
def cargar_usuarios():
    usuarios = {}
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                if len(datos) == 5:
                    usuario = datos[3]
                    usuarios[usuario] = {
                        "nombre": datos[0],
                        "id": datos[1],
                        "edad": datos[2],
                        "contrasena": datos[4]
                    }
    return usuarios
def guardar_usuario(nombre, identificacion, edad, usuario, contrasena):
    try:
        with open("usuarios.txt", "a") as archivo:
            archivo.write(f"{nombre},{identificacion},{edad},{usuario},{contrasena}\n")
            return True
    except:
        print("No se pudo guardar el usuario")
        return False
#administrador     
def menu_administrador():
    while True:
        print("-----Administrador - Polidelivery-----")
        print("1. Agregar nuevo centro de distribucion")
        print("2. Listar centros (ordenados)")
        print("3. Listar rutas (ordenadas)")
        print("4. Consultar centro especifico")
        print("5. Actualizar información de centro")
        print("6. Eliminar centro")
        print("7. Eliminar ruta")
        print("8. Guardar cambios")
        print("0. Salir")
        
        opcion = input("\nSeleccione una opcion: ")

def main():
    print("SISTEMA POLIDELIVERY")    
    while True:
        print("\n1. Registrarse")
        print("2. Iniciar sesion")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opcion: ")
