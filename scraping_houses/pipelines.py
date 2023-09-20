from itemadapter import ItemAdapter
import pymongo

class ScrapingHousesPipeline:
    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        self.db_casas = self.conn['Data_casas']
        self.collection_ventas_casas = self.db_casas['Ventas']
        self.collection_arriendo_casas = self.db_casas['Arriendo']

        self.db_departamentos = self.conn['Data_departamentos']
        self.collection_ventas_departamentos = self.db_departamentos['Ventas']
        self.collection_arriendo_departamentos = self.db_departamentos['Arriendo']
    def process_item(self, item, spider):
        if item['tipo'] == 'venta':
            if item['propiedad'] == 'casa':
                self.collection_ventas_casas.insert_one(dict(item))
            elif item['propiedad'] == 'departamento':
                self.collection_ventas_departamentos.insert_one(dict(item))
        elif item['tipo'] == 'arriendo':
            if item['propiedad'] == 'casa':
                self.collection_arriendo_casas.insert_one(dict(item))
            elif item['propiedad'] == 'departamento':
                self.collection_arriendo_departamentos.insert_one(dict(item))
        return item
