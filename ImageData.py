# os nos permite trabajar con rutas y carpetas.
import os
# Importamos la configuracion y las funciones que da el profesor.
import cfg
# Pillow nos permite abrir las imagenes PNG.
from PIL import Image


class ImageData:
    # Al crear el objeto, preparamos las variables que vamos a utilizar.
    def __init__(self):
        # Cada UUID tiene su ruta, sus metadatos y sus dimensiones.
        self.imagenes = {}
        self.campos = ['Prompt', 'Model', 'Seed', 'CFG_Scale', 'Steps',
                       'Sampler', 'Generated', 'Created_Date']

    # Guardamos una imagen nueva, pero todavia no leemos sus metadatos.
    def add_image(self, uuid, file):
        # Solo entramos en este bloque cuando se cumple la condicion.
        if not uuid or not file:
            # Salimos del metodo sin continuar con los pasos siguientes.
            return
        # Unimos la carpeta de la coleccion con la ruta del archivo.
        ruta = os.path.join(cfg.get_root(), file)
        # Si el archivo no existe, no lo anadimos.
        if not os.path.isfile(ruta):
            # Salimos del metodo sin continuar con los pasos siguientes.
            return
        # Convertimos el UUID a texto para usar siempre el mismo tipo de clave.
        identificador = str(uuid)
        # Solo entramos en este bloque cuando se cumple la condicion.
        if identificador in self.imagenes:
            # Salimos del metodo sin continuar con los pasos siguientes.
            return
        datos = {'filename': file, 'dimensions': None}
        # Recorremos cada elemento para comprobarlo uno a uno.
        for campo in self.campos:
            datos[campo] = None
        self.imagenes[identificador] = datos

    # Borramos la entrada de la imagen y todos sus datos.
    def remove_image(self, uuid):
        # Quitamos el elemento indicado; en una cola, pop quita el ultimo.
        self.imagenes.pop(str(uuid), None)

    # Leemos el PNG y actualizamos sus metadatos en memoria.
    def load_metadata(self, uuid):
        # Convertimos el UUID a texto para usar siempre el mismo tipo de clave.
        identificador = str(uuid)
        # Comprobamos que el elemento no este guardado o repetido.
        if identificador not in self.imagenes:
            # Salimos del metodo sin continuar con los pasos siguientes.
            return
        datos = self.imagenes[identificador]
        # Unimos la carpeta de la coleccion con la ruta del archivo.
        ruta = os.path.join(cfg.get_root(), datos['filename'])
        # Leemos los metadatos con la funcion oficial de cfg.
        metadatos = cfg.read_png_metadata(ruta)
        # Comprobamos si falta el dato antes de intentar utilizarlo.
        if metadatos is None:
            # Creamos un diccionario vacio para relacionar claves con sus datos.
            metadatos = {}
        # Se actualizan todos los campos, incluso si alguno ha desaparecido.
        for campo in self.campos:
            # get consulta el diccionario sin dar error si la clave no existe.
            valor = metadatos.get(campo)
            # Comprobamos si falta el dato antes de intentar utilizarlo.
            if valor is None:
                datos[campo] = 'None'
            else:
                datos[campo] = str(valor)
        # Intentamos hacer la operacion y controlamos los posibles errores.
        try:
            # Al salir de este bloque, el archivo o la imagen se cierra automaticamente.
            with Image.open(ruta) as imagen:
                datos['dimensions'] = imagen.size
        except (OSError, ValueError):
            datos['dimensions'] = (None, None)

    # Este metodo auxiliar consulta un campo sin repetir el mismo codigo.
    def _get_campo(self, uuid, campo):
        # Convertimos el UUID a texto para usar siempre el mismo tipo de clave.
        datos = self.imagenes.get(str(uuid))
        # Comprobamos si falta el dato antes de intentar utilizarlo.
        if datos is None:
            # Salimos del metodo sin continuar con los pasos siguientes.
            return None
        return datos[campo]

    # Devolvemos la ruta que guardamos al anadir la imagen.
    def get_filename(self, uuid):
        # Convertimos el UUID a texto para usar siempre el mismo tipo de clave.
        datos = self.imagenes.get(str(uuid))
        # Comprobamos si falta el dato antes de intentar utilizarlo.
        if datos is None:
            # Salimos del metodo sin continuar con los pasos siguientes.
            return None
        return datos['filename']

    # Consultamos el ancho y el alto que tenemos guardados.
    def get_dimensions(self, uuid):
        # Convertimos el UUID a texto para usar siempre el mismo tipo de clave.
        datos = self.imagenes.get(str(uuid))
        # Comprobamos si falta el dato antes de intentar utilizarlo.
        if datos is None:
            # Salimos del metodo sin continuar con los pasos siguientes.
            return None
        return datos['dimensions']

    # Obtenemos una lista de los identificadores para poder recorrer las imagenes.
    def get_uuids(self):
        # La busqueda necesita recorrer los identificadores guardados.
        return list(self.imagenes)

    # len(objeto) devuelve cuantos elementos hay guardados, no su espacio en memoria.
    def __len__(self):
        # len cuenta los elementos; str convierte ese numero a texto si hace falta.
        return len(self.imagenes)

    # Preparamos un texto sencillo para poder imprimir el objeto.
    def __str__(self):
        # len cuenta los elementos; str convierte ese numero a texto si hace falta.
        return 'ImageData: ' + str(len(self)) + ' imagenes'

    # Consultamos el campo prompt de la imagen.
    def get_prompt(self, uuid):
        return self._get_campo(uuid, 'Prompt')

    # Consultamos el campo modelo de la imagen.
    def get_model(self, uuid):
        return self._get_campo(uuid, 'Model')

    # Consultamos el campo semilla de la imagen.
    def get_seed(self, uuid):
        return self._get_campo(uuid, 'Seed')

    # Consultamos el campo CFG Scale de la imagen.
    def get_cfg_scale(self, uuid):
        return self._get_campo(uuid, 'CFG_Scale')

    # Consultamos el campo numero de pasos de la imagen.
    def get_steps(self, uuid):
        return self._get_campo(uuid, 'Steps')

    # Consultamos el campo sampler de la imagen.
    def get_sampler(self, uuid):
        return self._get_campo(uuid, 'Sampler')

    # Consultamos el campo indicador de generacion de la imagen.
    def get_generated(self, uuid):
        return self._get_campo(uuid, 'Generated')

    # Consultamos el campo fecha de creacion de la imagen.
    def get_created_date(self, uuid):
        return self._get_campo(uuid, 'Created_Date')
