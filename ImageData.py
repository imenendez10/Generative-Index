import os
import cfg
from PIL import Image


class ImageData:
    def __init__(self):
        # Cada UUID tiene su ruta, sus metadatos y sus dimensiones.
        self.imagenes = {}
        self.campos = ['Prompt', 'Model', 'Seed', 'CFG_Scale', 'Steps',
                       'Sampler', 'Generated', 'Created_Date']

    def add_image(self, uuid, file):
        identificador = str(uuid)
        if identificador in self.imagenes:
            return
        datos = {'filename': file, 'dimensions': (None, None)}
        for campo in self.campos:
            datos[campo] = 'None'
        self.imagenes[identificador] = datos

    def remove_image(self, uuid):
        self.imagenes.pop(str(uuid), None)

    def load_metadata(self, uuid):
        identificador = str(uuid)
        if identificador not in self.imagenes:
            return
        datos = self.imagenes[identificador]
        ruta = os.path.join(cfg.get_root(), datos['filename'])
        metadatos = cfg.read_png_metadata(ruta)
        if metadatos is None:
            metadatos = {}
        # Se actualizan todos los campos, incluso si alguno ha desaparecido.
        for campo in self.campos:
            valor = metadatos.get(campo)
            if valor is None:
                datos[campo] = 'None'
            else:
                datos[campo] = str(valor)
        try:
            with Image.open(ruta) as imagen:
                datos['dimensions'] = imagen.size
        except (OSError, ValueError):
            datos['dimensions'] = (None, None)

    def _get_campo(self, uuid, campo):
        datos = self.imagenes.get(str(uuid))
        if datos is None:
            return 'None'
        return datos[campo]

    def get_filename(self, uuid):
        datos = self.imagenes.get(str(uuid))
        if datos is None:
            return None
        return datos['filename']

    def get_dimensions(self, uuid):
        datos = self.imagenes.get(str(uuid))
        if datos is None:
            return (None, None)
        return datos['dimensions']

    def get_uuids(self):
        # La busqueda necesita recorrer los identificadores guardados.
        return list(self.imagenes)

    def __len__(self):
        return len(self.imagenes)

    def __str__(self):
        return 'ImageData: ' + str(len(self)) + ' imagenes'

    def get_prompt(self, uuid):
        return self._get_campo(uuid, 'Prompt')

    def get_model(self, uuid):
        return self._get_campo(uuid, 'Model')

    def get_seed(self, uuid):
        return self._get_campo(uuid, 'Seed')

    def get_cfg_scale(self, uuid):
        return self._get_campo(uuid, 'CFG_Scale')

    def get_steps(self, uuid):
        return self._get_campo(uuid, 'Steps')

    def get_sampler(self, uuid):
        return self._get_campo(uuid, 'Sampler')

    def get_generated(self, uuid):
        return self._get_campo(uuid, 'Generated')

    def get_created_date(self, uuid):
        return self._get_campo(uuid, 'Created_Date')
