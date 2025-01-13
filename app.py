from flask import Flask, request, jsonify
from threading import Thread
from queue import Queue
from Database.WooComerce import Woocomerce_db
from Schema.Store import WooCommerceConfigSchema
from Scraper.Amazon import amaz_scraper
from Scraper.Warlmart import main
from utilis.Collectstore import Extractstore
from Scraper.Temu import Temu
from pydantic import ValidationError
from flask_cors import CORS
from bson import json_util
import json

db = Woocomerce_db()

# Create collections
storecollection = db['stores']

# Initialize the Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.get('/')
def Home():
    '''
    Test base API
    '''
    return 'App Started'



@app.post('/api/Store')
def add_store():
    '''
    Configure store API
    '''
    try:
        if request.method == 'GET':
            return jsonify({"error": "Method not allowed"}), 405
        if storecollection is None:
            raise Exception('Database connection failed')
        data = request.json
        if not data:
            return jsonify({'message':'Data Not Given'}),400
        store_data = WooCommerceConfigSchema(**data)

        result = storecollection.insert_one(store_data.dict())
        return jsonify({'message': 'Data stored in database', 'id': str(result.inserted_id)}), 201

    except ValidationError as ve:
        return jsonify({"error": ve.errors()}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post('/api/EditKeywords')
def Edit_Keywords():
    try:
        if request.method != 'POST':
            return jsonify({'message':'Such Method Not Allowed'}),404
        else:
            data = request.json
            if not data:
                return jsonify({'message':'Data Not Given'}),400    
            else:
                store_id=data['store_id']
                store_data=storecollection.find_one({"store_id":store_id})
                if not store_data:
                    return jsonify({'message':'Store not found'}),400
                else:
                    storecollection.find_one_and_update({"store_id":store_id},
                        {"$set": data}
                    )
                    return jsonify({'message':'keywords updated'}),200

    except Exception as e:
        return jsonify({'errors':str(e)}) ,500   

@app.get('/api/showstores')
def ShowStores():
    try:
        store_collection=list(storecollection.find())
        if not store_collection:
            return jsonify({'message':'failed to fetch stores'}),400
        else:
            data = json_util.dumps(store_collection)
            return jsonify({'stores':data}),200    
    except Exception as e:
        return jsonify({'errors':str(e)}),500    

def process_scraper(scraper_func, queue):
    '''
    Run the scraper and notify when done
    '''
    try:
        scraper_func()
        queue.put("completed")  # Signal completion
    except Exception as e:
        queue.put(f"error: {e}")


def process_amazon_scraper():
    '''
    Amazon scraper logic
    '''
    stores = Extractstore()
    for store_id in stores:
        if store_id:
            categories = store_id.get('categories', [])
            amazon_keywords = next(
                (category['keywords'] for category in categories if category['paltform'].lower() == 'amazon'),
                []
            )
            api_sec, api_key, api_url = store_id['api_secret'], store_id['api_key'], store_id['domain']
            amaz_scraper(amazon_keywords, api_sec, api_key, api_url)


@app.get('/api/Amazon')
def call_amazon_scraper():
    '''
    Call Amazon scraper
    '''
    queue = Queue()
    thread = Thread(target=process_scraper, args=(process_amazon_scraper, queue))
    thread.start()
    thread.join()  # Wait for the thread to finish

    result = queue.get()
    if result == "completed":
        return jsonify({'message': 'Amazon scraper completed successfully'}), 200
    else:
        return jsonify({'error': result}), 500


def process_warlmart_scraper():
    '''
    Walmart scraper logic
    '''
    stores = Extractstore()
    for store_id in stores:
        if store_id:
            categories = store_id.get('categories', [])
            warlmart_keys = next(
                (category['keywords'] for category in categories if category['paltform'].lower() == 'walmart'),
                []
            )
            api_sec, api_key, api_url = store_id['api_secret'], store_id['api_key'], store_id['domain']
            main(warlmart_keys, api_sec, api_key, api_url)


@app.get('/api/Warlmart')
def call_warlmart_scraper():
    '''
    Call Walmart scraper
    '''
    print('---')
    queue = Queue()
    thread = Thread(target=process_scraper, args=(process_warlmart_scraper, queue))
    thread.start()
    thread.join()  # Wait for the thread to finish

    result = queue.get()
    if result == "completed":
        return jsonify({'message': 'Walmart scraper completed successfully'}), 200
    else:
        return jsonify({'error': result}), 500


def process_temu_scraper():
    try:
        stores = Extractstore()
        for store_id in stores:
            if store_id:
                categories = store_id.get('categories', [])
                Temukeys = next(
                    (category['keywords'] for category in categories if category['paltform'].lower() == 'temu'),
                    []
                )
                api_sec, api_key, api_url = store_id['api_secret'], store_id['api_key'], store_id['domain']
                Temu(Temukeys, api_sec, api_key, api_url)
    except Exception as e:
        print('error While process temu scraper',e)    

# api for temu scraper
@app.get('/api/Temu')
def call_temu_scraper():
    try:
        queue=Queue()
        thread=Thread(target=process_scraper,args=(process_temu_scraper,queue))
        thread.start()
        thread.join()  # Wait for the thread to finish

        result = queue.get()
        if result == "completed":
            return jsonify({'message': 'Temu scraper completed successfully'}), 200
        else:
            return jsonify({'error': result}), 500
    except Exception as e:
        print(e)    

@app.errorhandler(404)
def page_not_found(e):
    '''
    Error handler
    '''
    return jsonify({"error": "Endpoint not found"}), 404



