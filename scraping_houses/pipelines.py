from itemadapter import ItemAdapter
import pymongo

class ScrapingHousesPipeline:
    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )

        self.db_semanal = self.conn['Data_semanal']
        self.collection_ventas_casas = self.db_semanal['Venta_casas']
        self.collection_arriendo_casas = self.db_semanal['Arriendo_casas']
        self.collection_ventas_departamentos = self.db_semanal['Venta_departamentos']
        self.collection_arriendo_departamentos = self.db_semanal['Arriendo_departamentos']
        
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
