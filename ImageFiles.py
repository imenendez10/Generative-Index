import os
import cfg


class ImageFiles:
    def __init__(self):
        self.archivos = set()
        self.anadidos = []
        self.eliminados = []

    def reload_fs(self, path):
        nuevos_archivos = set()
        # os.walk tambien recorre las carpetas que hay dentro.
        for carpeta, subcarpetas, nombres in os.walk(path):
            for nombre in nombres:
                if nombre.lower().endswith('.png'):
                    ruta = os.path.join(carpeta, nombre)
                    ruta_relativa = cfg.get_canonical_pathfile(ruta)
                    nuevos_archivos.add(ruta_relativa)

        # Comparamos la lectura actual con la anterior.
        self.anadidos = sorted(nuevos_archivos - self.archivos)
        self.eliminados = sorted(self.archivos - nuevos_archivos)
        self.archivos = nuevos_archivos

    def files_added(self):
        return self.anadidos.copy()

    def files_removed(self):
        return self.eliminados.copy()

    def __str__(self):
        return 'ImageFiles: ' + str(len(self.archivos)) + ' archivos PNG'
