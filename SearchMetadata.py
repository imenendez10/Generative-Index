# Importamos la configuracion y las funciones que da el profesor.
import cfg


class SearchMetadata:
    # Al crear el objeto, preparamos las variables que vamos a utilizar.
    def __init__(self, image_data):
        self.image_data = image_data

    # Buscamos un texto dentro del campo indicado de cada imagen.
    def _buscar(self, sub, campo):
        # Empezamos con una lista vacia donde guardaremos los resultados.
        resultados = []
        # No pasamos a minusculas: las busquedas distinguen mayusculas.
        for identificador in self.image_data.get_uuids():
            valor = self.image_data._get_campo(identificador, campo)
            # Solo entramos en este bloque cuando se cumple la condicion.
            if valor is not None and valor != 'None' and str(sub) in valor:
                # Anadimos este elemento al final y conservamos el orden.
                resultados.append(identificador)
        return resultados

    # Buscamos imagenes con exactamente este ancho y este alto.
    def dimensions(self, width, height):
        # Empezamos con una lista vacia donde guardaremos los resultados.
        resultados = []
        # Recorremos cada elemento para comprobarlo uno a uno.
        for identificador in self.image_data.get_uuids():
            # Solo entramos en este bloque cuando se cumple la condicion.
            if self.image_data.get_dimensions(identificador) == (width, height):
                # Anadimos este elemento al final y conservamos el orden.
                resultados.append(identificador)
        return resultados

    # Nos quedamos con los identificadores que aparecen en las dos listas.
    def and_operator(self, list1, list2):
        # Empezamos con una lista vacia donde guardaremos los resultados.
        resultados = []
        ids_segunda = set(list2)
        # Creamos un conjunto vacio: no permite elementos repetidos.
        vistos = set()
        # Recorremos cada elemento para comprobarlo uno a uno.
        for identificador in list1:
            # Comprobamos que el elemento no este guardado o repetido.
            if identificador in ids_segunda and identificador not in vistos:
                # Anadimos este elemento al final y conservamos el orden.
                resultados.append(identificador)
                # Guardamos el elemento en el conjunto, sin duplicarlo.
                vistos.add(identificador)
        return resultados

    # Juntamos las dos listas sin repetir identificadores.
    def or_operator(self, list1, list2):
        # Empezamos con una lista vacia donde guardaremos los resultados.
        resultados = []
        # Creamos un conjunto vacio: no permite elementos repetidos.
        vistos = set()
        # Recorremos cada elemento para comprobarlo uno a uno.
        for identificador in list1 + list2:
            # Comprobamos que el elemento no este guardado o repetido.
            if identificador not in vistos:
                # Anadimos este elemento al final y conservamos el orden.
                resultados.append(identificador)
                # Guardamos el elemento en el conjunto, sin duplicarlo.
                vistos.add(identificador)
        return resultados

    # Preparamos un texto sencillo para poder imprimir el objeto.
    def __str__(self):
        # len cuenta los elementos; str convierte ese numero a texto si hace falta.
        return 'SearchMetadata: ' + str(len(self.image_data)) + ' imagenes disponibles'

    # Buscamos el texto dentro del campo prompt.
    def prompt(self, sub):
        return self._buscar(sub, 'Prompt')

    # Buscamos el texto dentro del campo modelo.
    def model(self, sub):
        return self._buscar(sub, 'Model')

    # Buscamos el texto dentro del campo semilla.
    def seed(self, sub):
        return self._buscar(sub, 'Seed')

    # Buscamos el texto dentro del campo CFG Scale.
    def cfg_scale(self, sub):
        return self._buscar(sub, 'CFG_Scale')

    # Buscamos el texto dentro del campo numero de pasos.
    def steps(self, sub):
        return self._buscar(sub, 'Steps')

    # Buscamos el texto dentro del campo sampler.
    def sampler(self, sub):
        return self._buscar(sub, 'Sampler')

    # Buscamos el texto dentro del campo indicador de generacion.
    def generated(self, sub):
        return self._buscar(sub, 'Generated')

    # Buscamos el texto dentro del campo fecha de creacion.
    def date(self, sub):
        return self._buscar(sub, 'Created_Date')
