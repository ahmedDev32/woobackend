from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
import os

load_dotenv()

def Woocomerce_db():
    '''
    create connection of db with project 
    '''
    try:
        uri=os.getenv('MONGOOSE_URL')
        if not uri:
            raise ValueError('Mongo URI IS NOT FOUND')

        CA_SSL_VER = certifi.where()
        Client=MongoClient(uri,tls=True,tlsCAFile=CA_SSL_VER,serverSelectionTimeoutMS=50000)
        db=Client['Woocomerce_db']
        return db
        
    except Exception as e:
        print('Error Occur while building connection with database',e)    
        return None