from woocommerce import API
from urllib.parse import urlparse, urlunparse

def remove_query_from_url(url):
    """
    Removes the query string from the URL if present.
    """
    parsed_url = urlparse(url)
    url_without_query = urlunparse(parsed_url._replace(query=""))
    return url_without_query

def woostore(data, api_url, key, secret, excluded=True):
    """
    Sync product data to WooCommerce.
    """
    try:
        # Initialize the WooCommerce API client
        wcapi = API(
            url=api_url,
            consumer_key=key,
            consumer_secret=secret,
            version="wc/v3",
            timeout=100
        )

        # Fetch the list of products
        get_products = wcapi.get('products')
        
        # Create a new product if not found
        result = wcapi.post("products", data)
        if result.status_code == 201:
            print("Product successfully created!")
            print(result.json())
        else:
            print(f"Failed to create product. Status code: {result.status_code}")
            print(result.json())
    except Exception as e:
        print("Error in syncing to WooCommerce:", e)

# Sample data for the product
data = {
    "name": "Custom Name Stamp with Dinosaur Design, Resin Material, Plain Ruling, Blue, with Personalized Gift Packaging for Clothing and Fabrics",
    "description": "Custom name stamp with dinosaur design resin material plain blue with personalized gift packaging for clothing and fabrics",
    "regular_price": "$4.10",
    "stock_status": "instock",
    "product_url": "https://example.com/goods.html?_bg_fs=1&goods_id=601099577431995&_oak_mp_inf=ELuvpram1ogBGiBhNjkzZDE3MTk3YTM0NTg5YWY0NGUwOTVjYTcyYjNmZCD76OS1xTI%3D&top_gallery_url=https%3A%2F%2Fimg.kwcdn.com%2Fproduct%2Ffancy%2Ff70fd66a-5516-4050-9288-4fc8e7f95296.jpg&spec_gallery_id=601099577431995&refer_page_sn=10005&refer_source=0&freesia_scene=1&_oak_freesia_scene=1&_oak_rec_ext_1=NDEw&_oak_gallery_order=391270053%2C1332167590%2C488334252%2C791968313%2C110677282",
    "images": [
        {"src": "https://aimg.kwcdn.com/upload_aimg/temu/35218716-bd3d-4f5a-8877-9771d5140ddd.png.slim.png"},
        {"src": "https://img.kwcdn.com/product/fancy/f70fd66a-5516-4050-9288-4fc8e7f95296.jpg"},
        {"src": "https://img.kwcdn.com/product/5a8100eb08d4304fdbbcd4d294ad0a2f43d409fa.goods.000001.jpeg"}
    ],
    "attributes": [
        {"name": "Size", "options": ["Small", "Medium", "Large"]},
        {"name": "Color", "options": ["Blue", "Green", "Red"]}
    ]
}

# Calling the function
woostore(data,"https://thcnoid.com/", "ck_73e8a2defbba193bf5ba9715c01195cfd586fe0e", "cs_07fe487da7cf1602f070652cf18a0227d06aee66")
