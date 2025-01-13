from Database.WooComerce import Woocomerce_db

db=Woocomerce_db()
store=db['stores']

def Extractstore():
    try:
        collectstore=store.find()
        return list(collectstore)
    except Exception as e:
        print('error Occuured',e)    
