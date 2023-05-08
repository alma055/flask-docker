import csv
columnas = []
def abrir_archivo(nombre_archivo):
    registros = []
    with open(nombre_archivo, "r", encoding="utf8") as archivo_csv:
        lectura_archivo = csv.DictReader(archivo_csv)
        for fila in lectura_archivo:
            registros.append(fila)
    return registros

def buscar_dato(lista, dato_buscar):
    resultado = 0
    for dato in lista:
        if dato['siglas'] == (dato_buscar):
            resultado = dato
    return resultado

def guardar_archivo(nombre_archivo, lista):
    with open(nombre_archivo, "w", encoding='utf8', newline='') as archivo_csv:
        escrito = csv.DictWriter(archivo_csv, fieldnames=columnas)
        escrito.writeheader()
        for pelicula in lista:
            escrito.writerow(pelicula)