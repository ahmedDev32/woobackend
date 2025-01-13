from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
import os

load_dotenv()
uri=os.getenv('MONGOOSE_URL')
CA_SSL_VER = certifi.where()
Client=MongoClient(uri,tls=True,tlsCAFile=CA_SSL_VER,serverSelectionTimeoutMS=50000)
db=Client['Woocomerce_db']

def insertData(collectionname,data):
    try:
        coll=db[collectionname]
        log_scrapper=db['logger']
        ExistingData=coll.find_one({"product_url": data.get("product_url")})
        if ExistingData:
            coll.find_one_and_update({"product_url": data.get("product_url")},{"$set":data})
            log_scrapper.find_one_and_update({'producturl':data.get('product_url')},{'$set':{
                'status':'update'
            }})
            print('data Updated....')
            return True
        coll.insert_one(data)
        log_scrapper.insert_one({'producturl':data.get('product_url'),'status':'newlyadded'})
        return True
    except Exception as e:
        print('Db Error',e)   
      