import json
import os
from collections import deque
import cfg


class Gallery:
    def __init__(self, image_id, image_viewer):
        self.image_id = image_id
        self.image_viewer = image_viewer
        # Una deque permite quitar por ambos extremos sin desplazar elementos.
        self.imagenes = deque()
        self.nombre = ''
        self.descripcion = ''
        self.fecha = ''

    def load_file(self, file):
        try:
            with open(file, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
        except (OSError, ValueError) as error:
            print('No se puede cargar la galeria:', error)
            return
        if not isinstance(datos, dict) or not isinstance(datos.get('images'), list):
            print('Formato de galeria incorrecto')
            return
        self.imagenes.clear()
        self.nombre = datos.get('gallery_name', '')
        self.descripcion = datos.get('description', '')
        self.fecha = datos.get('created_date', '')
        for ruta in datos['images']:
            if not isinstance(ruta, str):
                continue
            identificador = self.image_id.get_uuid(ruta)
            # Algunos JSON incluyen el nombre de la carpeta de imagenes.
            if identificador is None:
                relativa = cfg.get_canonical_pathfile(ruta)
                identificador = self.image_id.get_uuid(relativa)
            if identificador is None:
                prefijo = os.path.basename(cfg.get_root()) + '/'
                if ruta.startswith(prefijo):
                    identificador = self.image_id.get_uuid(ruta[len(prefijo):])
            if identificador is not None:
                self.imagenes.append(identificador)

    def show(self):
        for identificador in self.imagenes:
            self.image_viewer.show_image(identificador, cfg.DISPLAY_MODE)

    def add_image_at_end(self, uuid):
        self.imagenes.append(str(uuid))

    def remove_first_image(self):
        if self.imagenes:
            self.imagenes.popleft()

    def remove_last_image(self):
        if self.imagenes:
            self.imagenes.pop()

    def __len__(self):
        return len(self.imagenes)

    def __str__(self):
        return 'Gallery: ' + self.nombre + ' (' + str(len(self)) + ' imagenes)'
