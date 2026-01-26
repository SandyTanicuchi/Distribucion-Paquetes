import os
import heapq
from collections import deque
import re

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

def contraseña_segura(password):

    if (re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password)):
        return True
    return False

def registrar_usuario():
    print("\n--- REGISTRO DE USUARIO ---")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    cedula = input("Cédula: ")
    edad = input("Edad: ")
    email = input("Correo (nombre.apellido@gmail.com): ")
    password = input("Contraseña: ")


    if not contraseña_segura(password):
        print("Contraseña insegura")
        return


    with open("usuarios.txt", "a") as f:
        f.write(f"{nombre},{apellido},{cedula},{edad},{email},{password},CLIENTE\n")


    print("Usuario registrado correctamente")


def iniciar_sesion():
    print("\n--- INICIO DE SESIÓN ---")
    email = input("Correo: ")
    password = input("Contraseña: ")


    if not os.path.exists("usuarios.txt"):
        print("No hay usuarios registrados")
        return None


    with open("usuarios.txt", "r") as f:
        for linea in f:
            datos = linea.strip().split(',')
            if datos[4] == email and datos[5] == password:
                print("Sesión iniciada")
                return datos[6]

    print("Credenciales incorrectas")
    return None


def leer_centros():
    centros = {}
    if os.path.exists("centros.txt"):
        with open("centros.txt", "r") as f:
            for linea in f:
                id, nombre, region, subregion = linea.strip().split(',')
                centros[int(id)] = nombre
    return centros

def agregar_centro():
    id = input("ID del centro: ")
    nombre = input("Nombre del centro: ")
    region = input("Región: ")
    subregion = input("Subregión: ")


    with open("centros.txt", "a") as f:
        f.write(f"{id},{nombre},{region},{subregion}\n")
    print("Centro agregado")

def mostrar_centros():
    print("\n--- CENTROS DE DISTRIBUCIÓN ---")
    centros = leer_centros()
    for id, nombre in centros.items():
        print(f"{id} -> {nombre}")

def leer_rutas():
    grafo = {}
    if os.path.exists("rutas.txt"):
        with open("rutas.txt", "r") as f:
            for linea in f:
                o, d, dist, costo = linea.strip().split(',')
                o = int(o)
                d = int(d)
                costo = float(costo)
                if o not in grafo:
                    grafo[o] = []
                if d not in grafo:
                    grafo[d] = []
                grafo[o].append((d, costo))
                grafo[d].append((o, costo))
    return grafo

def agregar_ruta():
    o = int(input("Centro origen (ID): "))
    d = int(input("Centro destino (ID): "))
    dist = input("Distancia: ")
    costo = input("Costo: ")
    with open("rutas.txt", "a") as f:
        f.write(f"{o},{d},{dist},{costo}\n")
    print(" Ruta agregada")

def Camino_corto(grafo, inicio, fin):
    cola = [(0, inicio, [])]
    visitados = set()

    while cola:
        costo, nodo, camino = heapq.heappop(cola)


        if nodo in visitados:
            continue


        camino = camino + [nodo]
        visitados.add(nodo)


        if nodo == fin:
            return costo, camino


        for vecino, peso in grafo.get(nodo, []):
            if vecino not in visitados:
                heapq.heappush(cola, (costo + peso, vecino, camino))


    return None, None

def menu_admin():
    while True:
        print("\n--- MENÚ ADMIN ---")
        print("1. Agregar centro")
        print("2. Agregar ruta")
        print("3. Ver centros")
        print("4. Salir")
        opcion = input("Opción: ")

        if opcion == '1':
            agregar_centro()
        elif opcion == '2':
            agregar_ruta()
        elif opcion == '3':
            mostrar_centros()
        elif opcion == '4':
            break

def menu_cliente():
    while True:
        print("\n--- MENÚ CLIENTE ---")
        print("1. Ver centros")
        print("2. Ruta más económica")
        print("3. Salir")
        op = input("Opción: ")

        if op == '1':
            mostrar_centros()
        elif op == '2':
            grafo = leer_rutas()
            inicio = int(input("Centro inicio: "))
            fin = int(input("Centro destino: "))
            costo, camino = Camino_corto(grafo, inicio, fin)
            if camino:
                print("Ruta óptima:", camino)
                print("Costo total:", costo)
            else:
                print("No existe ruta")
        elif op == '3':
            break


def main():
    while True:
        print("\n=== POLIDELIVERY ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Opción: ")

        if opcion == '1':
            registrar_usuario()
        elif opcion == '2':
            rol = iniciar_sesion()
            if rol == "ADMIN":
                menu_admin()
            elif rol == "CLIENTE":
                menu_cliente()
        elif opcion == '3':
            print("Adiós")
            break


main()
