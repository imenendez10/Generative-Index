class SearchMetadata:
    def __init__(self, image_data):
        self.image_data = image_data

    def _buscar(self, sub, campo):
        resultados = []
        # No pasamos a minusculas: las busquedas distinguen mayusculas.
        for identificador in self.image_data.get_uuids():
            valor = self.image_data._get_campo(identificador, campo)
            if str(sub) in valor:
                resultados.append(identificador)
        return resultados

    def dimensions(self, width, height):
        resultados = []
        for identificador in self.image_data.get_uuids():
            if self.image_data.get_dimensions(identificador) == (width, height):
                resultados.append(identificador)
        return resultados

    def and_operator(self, list1, list2):
        resultados = []
        ids_segunda = set(list2)
        vistos = set()
        for identificador in list1:
            if identificador in ids_segunda and identificador not in vistos:
                resultados.append(identificador)
                vistos.add(identificador)
        return resultados

    def or_operator(self, list1, list2):
        resultados = []
        vistos = set()
        for identificador in list1 + list2:
            if identificador not in vistos:
                resultados.append(identificador)
                vistos.add(identificador)
        return resultados

    def __str__(self):
        return 'SearchMetadata: ' + str(len(self.image_data)) + ' imagenes disponibles'

    def prompt(self, sub):
        return self._buscar(sub, 'Prompt')

    def model(self, sub):
        return self._buscar(sub, 'Model')

    def seed(self, sub):
        return self._buscar(sub, 'Seed')

    def cfg_scale(self, sub):
        return self._buscar(sub, 'CFG_Scale')

    def steps(self, sub):
        return self._buscar(sub, 'Steps')

    def sampler(self, sub):
        return self._buscar(sub, 'Sampler')

    def generated(self, sub):
        return self._buscar(sub, 'Generated')

    def date(self, sub):
        return self._buscar(sub, 'Created_Date')
