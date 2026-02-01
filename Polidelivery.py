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
    rol ="ADMIN" if email == "admin@admin" else "CLIENTE"
    with open("usuarios.txt", "a") as f:
        f.write(f"{nombre},{apellido},{cedula},{edad},{email},{password},{rol}\n")
    print("Usuario registrado correctamente")

def iniciar_sesion():
    print("\n--- Iniciar secion ---")
    email = input("Correo: ")
    password = input("Contraseña: ")
    if not os.path.exists("usuarios.txt"):
        print("No hay usuarios registrados")
        return None,None,None
    
    with open("usuarios.txt", "r") as f:
        for linea in f:
            datos = linea.strip().split(',')
            if len(datos)>=7 and datos [4]== email and datos[5] == password:
                print("Sesion iniciada")
                return datos[6],datos[0], datos[1]
    print("Credenciales incorrectas")
    return None, None, None

def leer_centros():
    centros = {}
    if os.path.exists("centros.txt"):
        with open("centros.txt", "r") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue  
                partes = linea.split(',')
                if len(partes) != 4:
                    print(f"Linea invalida ignorada: {linea}")
                    continue
                try:
                    id, nombre, region, subregion = partes
                    centros[int(id)] = (nombre, region, subregion)
                except:
                    continue
    return centros

def agregar_centro():
    id = input("ID del centro: ")
    nombre = input("Nombre del centro: ")
    region = input("Region: ")
    subregion = input("Subregion: ")
    with open("centros.txt", "a") as f:
        f.write(f"{id},{nombre},{region},{subregion}\n")
    print("Centro agregado")

def mostrar_centros():
    print("\n--- Centros de Distribucion---")
    centros = leer_centros()
    if not centros:
        print("No hay centros registrados.")
        return
    for id, (nombre, region, subregion) in centros.items():
        print(f"ID: {id} | Nombre: {nombre} | Region: {region} | Subregion: {subregion}")

def actualizar_centro():
    try:
        id = int(input("ID del centro a actualizar: "))
        centros = leer_centros()
        if id not in centros:
            print("Centro no encontrado")
            return
        nom, reg, sub = centros[id]
        nombre = input(f"Nombre ({nom}): ").strip() or nom
        region = input(f"Región ({reg}): ").strip() or reg
        subregion = input(f"Subregión ({sub}): ").strip() or sub
        centros[id] = (nombre, region, subregion)
        with open("centros.txt", "w") as f:
            for cid, (n,r,s) in centros.items():
                f.write(f"{cid},{n},{r},{s}\n")
        print("Centro actualizado")
    except:
        print("ID invalido.")

def eliminar_elemento():
    print("\n--- Eliminar ---")
    print("1. Eliminar centro")
    print("2. Eliminar ruta")
    opcion = input("Ingrese una opcion: ")
    
    if opcion == "1":
        try:
            id_c = int(input("ID del centro a eliminar: "))
            centros = leer_centros()
            if id_c not in centros:
                print("No encontrado")
                return
            del centros[id_c]
            with open("centros.txt", "w") as f:
                for cid, (n,r,s) in centros.items():
                    f.write(f"{cid},{n},{r},{s}\n")
            print("Centro eliminado")
        except:
            print("ID invalido.")
    
    elif opcion == "2":
        try:
            origen = int(input("Origen ID: "))
            destino = int(input("Destino ID: "))
            if not os.path.exists("rutas.txt"):
                print("No hay rutas")
                return
            with open("rutas.txt", "r") as f:
                lineas = f.readlines()
            with open("rutas.txt", "w") as f:
                eliminado = False
                for linea in lineas:
                    p = linea.strip().split(',')
                    if len(p) == 4 and ((int(p[0]), int(p[1])) in [(origen,destino), (destino,origen)]):
                        eliminado = True
                        continue
                    f.write(linea)
            print("Ruta eliminada" if eliminado else "Ruta no encontrada")
        except:
            print("Datos invalidos.")
    else:
        print("Opción invalida")

def leer_rutas():
    grafo = {}
    if os.path.exists("rutas.txt"):
        with open("rutas.txt", "r") as f:
            for linea in f:
                try:
                    o, d, dist, costo = linea.strip().split(',')
                    o, d = int(o), int(d)
                    dist, costo = float(dist), float(costo)

                    if o not in grafo:
                        grafo[o] = []
                    if d not in grafo:
                        grafo[d] = []

                    grafo[o].append((d, dist, costo))
                    grafo[d].append((o, dist, costo))
                except:
                    continue
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
        costo_acum, nodo, camino = heapq.heappop(cola)
        if nodo in visitados:
            continue
        camino = camino + [nodo]
        visitados.add(nodo)
        if nodo == fin:
            return costo_acum, camino
        for vecino, _,costo in grafo.get(nodo, []):
            if vecino not in visitados:
                heapq.heappush(cola, (costo_acum + costo, vecino, camino))
    return None, None
def bfs(grafo, inicio):
    visitados = {inicio}
    cola = deque([inicio])
    orden = []
    while cola:
        nodo = cola.popleft()
        orden.append(nodo)
        for vecino, _, _ in grafo.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)
    return orden

def dfs(grafo, inicio, visitados=None):
    if visitados is None:
        visitados = set()
    visitados.add(inicio)
    orden = [inicio]
    for vecino, _, _ in grafo.get(inicio, []):
        if vecino not in visitados:
            orden.extend(dfs(grafo, vecino, visitados))
    return orden  
class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []

def mostrar_arbol(nodo, nivel =0):
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
        sub_nodo = next((h for h in regiones[region].hijos if h.nombre == subregion), None)
        if not sub_nodo:
            sub_nodo = Nodo(subregion)
            regiones[region].hijos.append(sub_nodo)
        sub_nodo.hijos.append(Nodo(f"{nombre} (ID: {id_centro})"))
    return raiz

def merge_sort(centros_list):
    if len(centros_list) <= 1:
        return centros_list
    mid = len(centros_list) // 2
    izq = merge_sort(centros_list[:mid])
    der = merge_sort(centros_list[mid:])
    i = j = k = 0
    while i < len(izq) and j < len(der):
        if izq[i][1][0].lower() < der[j][1][0].lower():
            centros_list[k] = izq[i]; i += 1
        else:
            centros_list[k] = der[j]; j += 1
        k += 1
    centros_list[k:] = izq[i:] if i < len(izq) else der[j:]
    return centros_list
        
def buscar_centro(centros_list, nombre):
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

def mostrar_mapa():
    print("\n--- Mapa de conexiones ---")
    grafo = leer_rutas()
    for o in sorted(grafo):
        print(f"{o}:")
        for d, dist, costo in sorted(grafo[o]):
            if o < d:
                print(f"  - {d}  (dist:{dist:.1f}  costo:{costo:.2f})")

def menu_admin():
    while True:
        print("\n--- Menu Administrador ---")
        print("1. Agregar centro / ruta")
        print("2. Listar centros ")
        print("3. Buscar centro ")
        print("4. Actualizar centro")
        print("5. Eliminar (centro o ruta)")
        print("6. Ver mapa de conexiones")
        print("7. Ver arbol de regiones")
        print("8. Guaradar en centros.txt ")
        print("9. Salir")
        opcion = input("Ingrese una opcion: ")
        match opcion:
            case '1':
                sub = input("1=Centro  2=Ruta ")
                if sub == "1": agregar_centro()
                elif sub == "2": agregar_ruta()
            case '2':
                centros = leer_centros()
                centros_list = list(centros.items())
                centros_list = merge_sort(centros_list)
                print("\nCentros ordenados por nombre:")
                for id, (nombre, region, subregion) in centros_list:
                    print(f"ID: {id} | Nombre: {nombre} | Región: {region} | Subregión: {subregion}")
            case '3':
                nombre = input("Nombre del centro a buscar: ")
                resultado = buscar_centro(nombre)
                if resultado:
                    id_centro, (nombre_centro, region, subregion) = resultado
                    print(f"Encontrado: ID={id_centro}, Nombre={nombre_centro}, Region={region}, Subregión={subregion}")
                else:
                    print("Centro no encontrado ")
            case '4':
                actualizar_centro()
            case '5':
                eliminar_elemento()
            case '6':
                mostrar_mapa()
            case '7':
                arbol = arbol_regiones()
                mostrar_arbol(arbol)
            case '8':
                print("Guardando cambios ")
            case '9':
                print("Saliendo del sistema.")
                break
            case _:
                print("Opcion invalida.")

def menu_cliente(nombre, apellido):
    selecion=[]
    while True:
        print("\n--- Menu Cliente ---")
        print("1. Ver mapa de centros")
        print("2. Ruta economica entre dos centros")
        print("3. Ver arbol de regiones")
        print("4. Seleccionar centros para envio (min 2)")
        print("5. Ver selección y costo total")
        print("6. Ordenar seleccion ")
        print("7. Actualizar seleccion")
        print("8. Eliminar centros")
        print("9. Guardar en rutas-cliente.txt")
        print("10. Salir")
        op = input("Ingrese una opcion: ")

        if op == '1':
            mostrar_mapa()
        elif op == '2':
            mostrar_centros()
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
            arbol = arbol_regiones()
            mostrar_arbol(arbol)
        elif op == '4':
            mostrar_centros()
            txt = input("Ingrese IDs separados por coma (1,3,5): ")
            try:
                nuevos = [int(x.strip()) for x in txt.split(',') if x.strip()]
                if len(nuevos) < 2:
                    print("Debe seleccionar minimo dos centros")
                else:
                    seleccion = nuevos
                    print("Centros seleccionados:", seleccion)
            except:
                print("Formato invalido ")

        elif op == '5':
            if not seleccion:
                print("No ha seleccionado centros aun")
                continue
            print("\nCentros seleccionados:", seleccion)
            grafo = leer_rutas()
            costo_total = 0
            ruta_completa = True
            for i in range(len(seleccion)-1):
                c, _ = Camino_corto(grafo, seleccion[i], seleccion[i+1])
                if c is None:
                    print(f"No hay ruta entre {seleccion[i]} y {seleccion[i+1]}")
                    ruta_completa = False
                    break
                costo_total += c
            if ruta_completa:
                print(f"Costo total estimado: {costo_total}")
            else:
                print("No se puede calcular costo total (ruta incompleta)")

        elif op == '6':
            if not seleccion:
                print("No hay seleccion para ordenar")
                continue
            centros = leer_centros()
            lista = []
            for id_c in seleccion:
                if id_c in centros:
                    lista.append((id_c, centros[id_c]))
            if lista:
                lista = merge_sort(lista)
                seleccion = [item[0] for item in lista]
                print("Selección ordenada por nombre del centro:", seleccion)
            else:
                print("Ninguno de los IDs seleccionados existe")

        elif op == '7':
            txt = input("Ingrese nueva lista de IDs (coma separada) o Enter para mantener: ")
            if txt.strip():
                try:
                    nuevos = [int(x.strip()) for x in txt.split(',') if x.strip()]
                    if len(nuevos) < 2:
                        print("Minimo dos centros")
                    else:
                        seleccion = nuevos
                        print("Seleccion actualizada")
                except:
                    print("Formato invalido")
            else:
                print("Selección no modificada")

        elif op == '8':
            seleccion = []
            print("Todos los centros seleccionados han sido eliminados")

        elif op == '9':
            if not seleccion:
                print("No hay selección para guardar")
                continue
            archivo = f"rutas-{nombre}-{apellido}.txt"
            with open(archivo, "w") as f:
                f.write("Centros seleccionados para envio:\n")
                f.write(",".join(map(str, seleccion)) + "\n")
            print(f"Seleccion guardada en: {archivo}")

        elif op == '10':
            print("Saliendo...")
            break
        else:
            print("Opcion invalida")      
def main():
    while True:
        print("\n --- POLIDELIVERY ---")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == '1':
            registrar_usuario()
        elif opcion == '2':
            rol, nombre, apellido = iniciar_sesion()
            if rol == "ADMIN":
                menu_admin()
            elif rol == "CLIENTE":
                menu_cliente(nombre, apellido)
        elif opcion == '3':
            print("Hasta pronto...")
            break
main()
