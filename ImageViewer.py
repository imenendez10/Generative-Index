import os
import cfg
from PIL import Image


class ImageViewer:
    def __init__(self, image_data):
        self.image_data = image_data

    def print_image(self, uuid):
        archivo = self.image_data.get_filename(uuid)
        if archivo is None:
            return
        ancho, alto = self.image_data.get_dimensions(uuid)
        prompt = self.image_data.get_prompt(uuid)
        if len(prompt) > 100:
            prompt = prompt[:100] + '...'
        print('Archivo:', archivo)
        print('UUID:', uuid)
        print('Dimensions:', str(ancho) + 'x' + str(alto))
        print('Prompt:', prompt)
        print('Model:', self.image_data.get_model(uuid))
        print('Seed:', self.image_data.get_seed(uuid))
        print('CFG Scale:', self.image_data.get_cfg_scale(uuid))
        print('Steps:', self.image_data.get_steps(uuid))
        print('Sampler:', self.image_data.get_sampler(uuid))
        print('Generated:', self.image_data.get_generated(uuid))
        print('Created Date:', self.image_data.get_created_date(uuid))

    def show_file(self, file):
        ruta = os.path.join(cfg.get_root(), file)
        try:
            with Image.open(ruta) as imagen:
                imagen.show()
        except (OSError, ValueError) as error:
            print('No se puede mostrar la imagen:', error)

    def show_image(self, uuid, mode=None):
        if mode is None:
            mode = cfg.DISPLAY_MODE
        archivo = self.image_data.get_filename(uuid)
        if archivo is None:
            return
        if mode == 0 or mode == 1:
            self.print_image(uuid)
        if mode == 1 or mode == 2:
            self.show_file(archivo)
        # No usamos input porque bloquearia el corrector.

    def __str__(self):
        return 'ImageViewer: ' + str(len(self.image_data)) + ' imagenes disponibles'
