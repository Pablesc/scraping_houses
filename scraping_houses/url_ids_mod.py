import pymongo
import re

def obtener_url_ids():
    conn = pymongo.MongoClient('localhost', 27017 )
    
    db_casas = conn['Data_casas']
    db_deptos = conn['Data_departamentos']
    colec_ac, colec_vc = db_casas['Arriendo'], db_casas['Ventas']
    colec_ad, colec_vd = db_deptos['Arriendo'], db_deptos['Ventas']
    colecc = [colec_ac, colec_vc, colec_ad, colec_vd] 
    
    url_ids = {
            'ac': set(),
            'vc': set(),
            'ad': set(),
            'vd': set()
        }

    patron = r"MLC-[0-9]+"

    for colec in colecc:
        for documento in colec.find():
            url = documento.get("url")
            url_ = re.search(patron, url)
            url_id = url_.group()
            if colec == colec_ac:
                url_ids['ac'].add(url_id)
            elif colec == colec_vc:
                url_ids['vc'].add(url_id)
            elif colec == colec_ad:
                url_ids['ad'].add(url_id)
            elif colec == colec_vd:
                url_ids['vd'].add(url_id)

    conn.close()

    return url_ids
