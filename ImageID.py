# os nos permite trabajar con rutas y carpetas.
import os
# Importamos la configuracion y las funciones que da el profesor.
import cfg


class ImageID:
    # Al crear el objeto, preparamos las variables que vamos a utilizar.
    def __init__(self):
        # Creamos un diccionario vacio para relacionar claves con sus datos.
        self.ids_por_archivo = {}
        # Creamos un diccionario vacio para relacionar claves con sus datos.
        self.archivos_por_id = {}

    # Usamos una ruta relativa para identificar el mismo archivo siempre igual.
    def _ruta_relativa(self, file):
        # Dentro del programa usamos rutas relativas a la coleccion.
        if os.path.isabs(file):
            return cfg.get_canonical_pathfile(file)
        return os.path.normpath(file).replace(os.sep, '/')

    # Calculamos un UUID y comprobamos que nadie lo este utilizando.
    def generate_uuid(self, file):
        archivo = self._ruta_relativa(file)
        identificador = str(cfg.get_uuid(archivo))
        # Solo entramos en este bloque cuando se cumple la condicion.
        if identificador in self.archivos_por_id:
            print('UUID ya utilizado. Se ignora el archivo:', archivo)
            # Salimos del metodo sin continuar con los pasos siguientes.
            return None
        self.ids_por_archivo[archivo] = identificador
        self.archivos_por_id[identificador] = archivo
        return identificador

    # Buscamos el identificador que ya hemos guardado para este archivo.
    def get_uuid(self, file):
        archivo = self._ruta_relativa(file)
        return self.ids_por_archivo.get(archivo)

    # Quitamos el identificador para que se pueda volver a utilizar.
    def remove_uuid(self, uuid):
        # Convertimos el UUID a texto para usar siempre el mismo tipo de clave.
        identificador = str(uuid)
        # Solo entramos en este bloque cuando se cumple la condicion.
        if identificador in self.archivos_por_id:
            archivo = self.archivos_por_id.pop(identificador)
            del self.ids_por_archivo[archivo]

    # len(objeto) devuelve cuantos elementos hay guardados, no su espacio en memoria.
    def __len__(self):
        # len cuenta los elementos; str convierte ese numero a texto si hace falta.
        return len(self.archivos_por_id)

    # Preparamos un texto sencillo para poder imprimir el objeto.
    def __str__(self):
        # len cuenta los elementos; str convierte ese numero a texto si hace falta.
        return 'ImageID: ' + str(len(self)) + ' identificadores activos'
