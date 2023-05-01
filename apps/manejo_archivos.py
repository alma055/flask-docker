import csv

def abrir_archivo(nombre_archivo):
    registros = []
    with open(nombre_archivo, "r", encoding="utf8") as archivo_csv:
        lectura_archivo = csv.DictReader(archivo_csv)
        for fila in lectura_archivo:
            registros.append(fila)
    return registros
