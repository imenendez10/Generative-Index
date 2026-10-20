# os nos permite trabajar con rutas y carpetas.
import os
# Importamos la configuracion y las funciones que da el profesor.
import cfg
# Pillow nos permite abrir las imagenes PNG.
from PIL import Image


class ImageViewer:
    # Al crear el objeto, preparamos las variables que vamos a utilizar.
    def __init__(self, image_data):
        self.image_data = image_data

    # Mostramos los datos guardados sin volver a leer los metadatos del disco.
    def print_image(self, uuid):
        archivo = self.image_data.get_filename(uuid)
        # Comprobamos si falta el dato antes de intentar utilizarlo.
        if archivo is None:
            # Salimos del metodo sin continuar con los pasos siguientes.
            return
        dimensiones = self.image_data.get_dimensions(uuid)
        # Comprobamos si falta el dato antes de intentar utilizarlo.
        if dimensiones is None:
            dimensiones = (None, None)
        ancho, alto = dimensiones
        prompt = self.image_data.get_prompt(uuid)
        # Comprobamos si falta el dato antes de intentar utilizarlo.
        if prompt is None:
            prompt = 'None'
        # Solo entramos en este bloque cuando se cumple la condicion.
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

    # Abrimos el archivo con Pillow para mostrar la imagen.
    def show_file(self, file):
        # Unimos la carpeta de la coleccion con la ruta del archivo.
        ruta = os.path.join(cfg.get_root(), file)
        # Intentamos hacer la operacion y controlamos los posibles errores.
        try:
            # Al salir de este bloque, el archivo o la imagen se cierra automaticamente.
            with Image.open(ruta) as imagen:
                imagen.show()
        except (OSError, ValueError) as error:
            print('No se puede mostrar la imagen:', error)

    # Segun el modo, mostramos los metadatos, la imagen o ambas cosas.
    def show_image(self, uuid, mode=None):
        # Comprobamos si falta el dato antes de intentar utilizarlo.
        if mode is None:
            mode = cfg.DISPLAY_MODE
        archivo = self.image_data.get_filename(uuid)
        # Comprobamos si falta el dato antes de intentar utilizarlo.
        if archivo is None:
            # Salimos del metodo sin continuar con los pasos siguientes.
            return
        # Comprobamos que accion corresponde a este modo de visualizacion.
        if mode == 0 or mode == 1:
            self.print_image(uuid)
        # Comprobamos que accion corresponde a este modo de visualizacion.
        if mode == 1 or mode == 2:
            self.show_file(archivo)
        # No usamos input porque bloquearia el corrector.

    # Preparamos un texto sencillo para poder imprimir el objeto.
    def __str__(self):
        # len cuenta los elementos; str convierte ese numero a texto si hace falta.
        return 'ImageViewer: ' + str(len(self.image_data)) + ' imagenes disponibles'
