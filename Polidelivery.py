import os
import heapq
from collections import deque
import re
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
            if len(datos) >=7:
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
                centros[int(id)] = (nombre, region, subregion)
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
    for id, (nombre, region, subregion) in centros.items():
        print(f"ID: {id} -> {nombre} ({region} - {subregion})")

def leer_rutas():
    grafo = {}
    if os.path.exists("rutas.txt"):
        with open("rutas.txt", "r") as f:
            for linea in f:
                if len(partes) >= 4:
                    o, d, dist, costo = partes
                    o, d = int(o), int(d)
                    dist, costo = float(dist), float(costo)
                    
                    if o not in grafo:
                        grafo[o] = []
                    if d not in grafo:
                        grafo[d] = []
                    
                    grafo[o].append((d, dist, costo))
                    grafo[d].append((o, dist, costo))
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
    
def bfs(grafo, inicio):
    visitados = set()
    cola = deque([inicio])
    visitados.add(inicio)
    orden = []
    while cola:
        nodo = cola.popleft()
        orden.append(nodo)
        
        for vecino, _ in grafo.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino) 
    return orden

def dfs(grafo, inicio, visitados=None):
    if visitados is None:
        visitados = set()
    
    visitados.add(inicio)
    orden = [inicio]
    
    for vecino, _ in grafo.get(inicio, []):
        if vecino not in visitados:
            orden.extend(dfs(grafo, vecino, visitados))
    
    return orden
class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []
def mostrar_arbol(nodo, nivel=0):
    print("  " * nivel+ "- " + nodo.nombre)
    for hijo in nodo.hijos:
        mostrar_arbol(hijo, nivel + 1)

def arbol_regiones():
    raiz = Nodo("Ecuador")
    regiones = {}
    centros = leer_centros()
    for id_centro, (nombre, region, subregion) in centros.items():
        if region not in regiones:
            regiones[region] = Nodo(region)
            raiz.hijos.append(regiones[region])
        sub_nodo = None
        for hijo in regiones[region].hijos:
            if hijo.nombre == subregion:
                sub_nodo = hijo
                break
        
        if sub_nodo is None:
            sub_nodo = Nodo(subregion)
            regiones[region].hijos.append(sub_nodo)
        centro_nodo = Nodo(f"{nombre} (ID: {id_centro})")
        sub_nodo.hijos.append(centro_nodo)
    
    return raiz

def matriz_costos():
    centros= leer_centros()
    ids = list(centros.keys())
    g = leer_rutas()
    m = [[float('inf')] * len(ids) for _ in ids]
    for i in range(len(ids)):
        m[i][i] = 0
    for i, c in enumerate(ids):
        for vecino, costo in g.get(c, []):
            j = ids.index(vecino)
            m[i][j] = costo
    print("\nMatriz de costos:")
    for fila in m:
        print(fila)
        
def ordenar_centros():
    centros= leer_centros()
    centros_ordenados= sorted(leer_centros().items(), key=lambda x: x[1][0]):
    print("\n--- Centros ordenados ---")
    for id_centro,(nombre, region,subregion)in centros_oredenados:
        print(f"{id_centro}: {nombre}")

def buscar_centro(nombre):
    centros = leer_centros()
    centros_lista = sorted(centros.items(), key=lambda x: x[1][0].lower())
    inicio = 0
    fin = len(centros_lista) - 1
    
    while inicio <= fin:
        medio = (inicio + fin) // 2
        id_centro, (nombre_centro, region, subregion) = centros_lista[medio]
        
        if nombre_centro.lower() == nombre.lower():
            return (id_centro, (nombre_centro, region, subregion))
        elif nombre_centro.lower() < nombre.lower():
            inicio = medio + 1
        else:
            fin = medio - 1
    
    return None
def menu_admin():
    while True:
        print("\n--- Menu Administrador ---")
        print("1. Agregar centro")
        print("2. Agregar ruta")
        print("3. Ver centros")
        print("4. Ver arbol de regiones")
        print("5. Ver matriz de costos")
        print("6. Ordenar centros por nombre")
        print("7. Buscar centro")
        print("8. Salir")
        opcion = input("Ingrese una opción: ")
        match opcion:
            case '1':
                agregar_centro()
            case '2':
                agregar_ruta()
            case '3':
                mostrar_centros()
            case '4':
                arbol = arbol_regiones()
                mostrar_arbol(arbol)
            case '5':
                matriz_costos()
            case '6':
                ordenar_centros()
            case '7':
                nombre = input("Nombre del centro a buscar: ")
                resultado = buscar_centro(nombre)
                if resultado:
                    id_centro, (nombre_centro, region, subregion) = resultado
                    print(f"Encontrado: ID={id_centro}, Nombre={nombre_centro}, Región={region}, Subregión={subregion}")
                else:
                    print("Centro no encontrado")
            case '8':
                break
            case _:
                print("Opcion invalida.")


def menu_cliente():
    while True:
        print("\n--- Menu Cliente ---")
        print("1. Ver centros")
        print("2. Ruta mas economica")
        print("3. Ver recorrido BFS")
        print("4. Ver recorrido DFS")
        print("5. Salir")
        op = input("Ingrese una opcion: ")

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
            grafo = leer_rutas()
            inicio = int(input("Centro inicio (ID): "))
            orden = bfs(grafo, inicio)
            print("Recorrido BFS:", " -> ".join(str(nodo) for nodo in orden))
        elif op == '4':
            grafo = leer_rutas()
            inicio = int(input("Centro inicio (ID): "))
            orden = dfs(grafo, inicio)
            print("Recorrido DFS:", " -> ".join(str(nodo) for nodo in orden))
        elif op == '5':
            break
        
def main():
    while True:
        print("\n=== POLIDELIVERY ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Ingrese una opcion: ")

        if opcion == '1':
            registrar_usuario()
        elif opcion == '2':
            rol = iniciar_sesion()
            if rol == "ADMIN":
                menu_admin()
            elif rol == "CLIENTE":
                menu_cliente()
        elif opcion == '3':
            print("Adios")
            break
main()
