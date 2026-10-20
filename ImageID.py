import os
import cfg


class ImageID:
    def __init__(self):
        self.ids_por_archivo = {}
        self.archivos_por_id = {}

    def _ruta_relativa(self, file):
        # Dentro del programa usamos rutas relativas a la coleccion.
        if os.path.isabs(file):
            return cfg.get_canonical_pathfile(file)
        return os.path.normpath(file).replace(os.sep, '/')

    def generate_uuid(self, file):
        archivo = self._ruta_relativa(file)
        identificador = str(cfg.get_uuid(archivo))
        if identificador in self.archivos_por_id:
            print('UUID ya utilizado. Se ignora el archivo:', archivo)
            return None
        self.ids_por_archivo[archivo] = identificador
        self.archivos_por_id[identificador] = archivo
        return identificador

    def get_uuid(self, file):
        archivo = self._ruta_relativa(file)
        return self.ids_por_archivo.get(archivo)

    def remove_uuid(self, uuid):
        identificador = str(uuid)
        if identificador in self.archivos_por_id:
            archivo = self.archivos_por_id.pop(identificador)
            del self.ids_por_archivo[archivo]

    def __len__(self):
        return len(self.archivos_por_id)

    def __str__(self):
        return 'ImageID: ' + str(len(self)) + ' identificadores activos'
