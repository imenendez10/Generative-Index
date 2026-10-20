# os nos permite trabajar con rutas y carpetas.
import os
# Importamos la configuracion y las funciones que da el profesor.
import cfg


class ImageFiles:
    # Al crear el objeto, preparamos las variables que vamos a utilizar.
    def __init__(self):
        # Creamos un conjunto vacio: no permite elementos repetidos.
        self.archivos = set()
        # Empezamos con una lista vacia donde guardaremos los resultados.
        self.anadidos = []
        # Empezamos con una lista vacia donde guardaremos los resultados.
        self.eliminados = []

    # Volvemos a leer las carpetas y comprobamos que archivos han cambiado.
    def reload_fs(self, path):
        # Creamos un conjunto vacio: no permite elementos repetidos.
        nuevos_archivos = set()
        # os.walk tambien recorre las carpetas que hay dentro.
        for carpeta, subcarpetas, nombres in os.walk(path):
            # Recorremos cada elemento para comprobarlo uno a uno.
            for nombre in nombres:
                # Pasamos la extension a minusculas para aceptar tambien .PNG.
                if nombre.lower().endswith('.png'):
                    # Unimos la carpeta de la coleccion con la ruta del archivo.
                    ruta = os.path.join(carpeta, nombre)
                    # Calculamos la ruta desde la raiz de la coleccion y usamos barras /.
                    ruta_relativa = os.path.relpath(os.path.abspath(ruta), cfg.get_root()).replace(os.sep, '/')
                    # Guardamos el elemento en el conjunto, sin duplicarlo.
                    nuevos_archivos.add(ruta_relativa)

        # Comparamos la lectura actual con la anterior.
        self.anadidos = sorted(nuevos_archivos - self.archivos)
        # La diferencia de conjuntos detecta cambios; sorted los deja ordenados.
        self.eliminados = sorted(self.archivos - nuevos_archivos)
        self.archivos = nuevos_archivos

    # Consultamos que archivos aparecieron en la ultima lectura.
    def files_added(self):
        # Devolvemos una copia para que no puedan cambiar nuestra lista desde fuera.
        return self.anadidos.copy()

    # Consultamos que archivos desaparecieron en la ultima lectura.
    def files_removed(self):
        # Devolvemos una copia para que no puedan cambiar nuestra lista desde fuera.
        return self.eliminados.copy()

    # Preparamos un texto sencillo para poder imprimir el objeto.
    def __str__(self):
        # len cuenta los elementos; str convierte ese numero a texto si hace falta.
        return 'ImageFiles: ' + str(len(self.archivos)) + ' archivos PNG'
