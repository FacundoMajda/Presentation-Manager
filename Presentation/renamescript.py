import os
#ESTE ESCRIPT RENOMBRA TODOS LOS ARCHIVOS QUE ESTEN DENTRO DE ESTA CARPETA COMO "Slide[i]"
#Solo agrega mas variables al array de mas abajo
# Obtener la ruta del directorio actual donde se encuentra el script
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Lista de nombres de archivo deseados
nombres_archivos = ["Slide1", "Slide2", "Slide3", "Slide4", "Slide5", "Slide6"] #<---:)

# Obtener la lista de archivos en el directorio actual
archivos = os.listdir(directorio_actual)

# Filtrar solo los archivos de imagen (puedes ajustar la extensión si es necesario)
archivos_imagen = [archivo for archivo in archivos if archivo.endswith(
    (".jpg", ".png", ".jpeg"))]

# Verificar que el número de archivos coincida con la cantidad de nombres deseados
if len(archivos_imagen) != len(nombres_archivos):
    print("El número de archivos de imagen no coincide con la cantidad de nombres deseados.")
else:
    # Iterar sobre los archivos y renombrarlos
    for i in range(len(archivos_imagen)):
        nombre_original = archivos_imagen[i]
        nuevo_nombre = nombres_archivos[i] + \
            os.path.splitext(nombre_original)[1]
        ruta_original = os.path.join(directorio_actual, nombre_original)
        ruta_nuevo_nombre = os.path.join(directorio_actual, nuevo_nombre)
        os.rename(ruta_original, ruta_nuevo_nombre)
        print(f"Archivo {nombre_original} renombrado como {nuevo_nombre}")
