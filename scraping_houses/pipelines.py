from itemadapter import ItemAdapter
import pymongo

class ScrapingHousesPipeline:
    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['Data_casas']
        #self.collection = db['Ventas']
        self.collection = db['Prueba']

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item 
