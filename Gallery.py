# json nos permite leer el archivo que describe una galeria.
import json
# os nos permite trabajar con rutas y carpetas.
import os
# Usamos deque para anadir y quitar por los dos extremos.
from collections import deque
# Importamos la configuracion y las funciones que da el profesor.
import cfg


class Gallery:
    # Al crear el objeto, preparamos las variables que vamos a utilizar.
    def __init__(self, image_id, image_viewer):
        self.image_id = image_id
        self.image_viewer = image_viewer
        # Una deque permite quitar por ambos extremos sin desplazar elementos.
        self.imagenes = deque()
        self.nombre = ''
        self.descripcion = ''
        self.fecha = ''

    # Leemos el JSON y sustituimos el contenido de esta galeria.
    def load_file(self, file):
        # Cada carga sustituye la galeria anterior, aunque el archivo no exista.
        self.imagenes.clear()
        self.nombre = ''
        self.descripcion = ''
        self.fecha = ''
        # Intentamos hacer la operacion y controlamos los posibles errores.
        try:
            # Al salir de este bloque, el archivo o la imagen se cierra automaticamente.
            with open(file, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
        except (OSError, ValueError) as error:
            print('No se puede cargar la galeria:', error)
            # Salimos del metodo sin continuar con los pasos siguientes.
            return
        # Solo entramos en este bloque cuando se cumple la condicion.
        if not isinstance(datos, dict) or not isinstance(datos.get('images'), list):
            print('Formato de galeria incorrecto')
            # Salimos del metodo sin continuar con los pasos siguientes.
            return
        # Vaciamos lo que habia guardado antes.
        self.imagenes.clear()
        # get consulta el diccionario sin dar error si la clave no existe.
        self.nombre = datos.get('gallery_name', '')
        # get consulta el diccionario sin dar error si la clave no existe.
        self.descripcion = datos.get('description', '')
        # get consulta el diccionario sin dar error si la clave no existe.
        self.fecha = datos.get('created_date', '')
        # Recorremos cada elemento para comprobarlo uno a uno.
        for ruta in datos['images']:
            # Solo entramos en este bloque cuando se cumple la condicion.
            if not isinstance(ruta, str):
                continue
            identificador = self.image_id.get_uuid(ruta)
            # Algunos JSON incluyen el nombre de la carpeta de imagenes.
            if identificador is None:
                relativa = cfg.get_canonical_pathfile(ruta)
                identificador = self.image_id.get_uuid(relativa)
            # Comprobamos si falta el dato antes de intentar utilizarlo.
            if identificador is None:
                prefijo = os.path.basename(cfg.get_root()) + '/'
                # Solo entramos en este bloque cuando se cumple la condicion.
                if ruta.startswith(prefijo):
                    identificador = self.image_id.get_uuid(ruta[len(prefijo):])
            # Solo entramos en este bloque cuando se cumple la condicion.
            if identificador is not None:
                # Anadimos este elemento al final y conservamos el orden.
                self.imagenes.append(identificador)

    # Recorremos las imagenes de la galeria en el orden guardado.
    def show(self):
        # Recorremos cada elemento para comprobarlo uno a uno.
        for identificador in self.imagenes:
            self.image_viewer.show_image(identificador, cfg.DISPLAY_MODE)

    # Anadimos el identificador al final de la galeria.
    def add_image_at_end(self, uuid):
        # Anadimos este elemento al final y conservamos el orden.
        self.imagenes.append(str(uuid))

    # Quitamos la primera imagen si la galeria no esta vacia.
    def remove_first_image(self):
        # Solo entramos en este bloque cuando se cumple la condicion.
        if self.imagenes:
            # Eliminamos el primer elemento de la cola.
            self.imagenes.popleft()

    # Quitamos la ultima imagen si la galeria no esta vacia.
    def remove_last_image(self):
        # Solo entramos en este bloque cuando se cumple la condicion.
        if self.imagenes:
            # Quitamos el elemento indicado; en una cola, pop quita el ultimo.
            self.imagenes.pop()

    # len(objeto) devuelve cuantos elementos hay guardados, no su espacio en memoria.
    def __len__(self):
        # len cuenta los elementos; str convierte ese numero a texto si hace falta.
        return len(self.imagenes)

    # Preparamos un texto sencillo para poder imprimir el objeto.
    def __str__(self):
        # len cuenta los elementos; str convierte ese numero a texto si hace falta.
        return 'Gallery: ' + self.nombre + ' (' + str(len(self)) + ' imagenes)'
