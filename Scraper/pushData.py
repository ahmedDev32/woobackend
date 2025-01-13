from woocommerce import API
from urllib.parse import urlparse, urlunparse, parse_qs

def remove_query_from_url(url):
    """
    Removes the query string from the URL if present.
    """
    parsed_url = urlparse(url)
    url_without_query = urlunparse(parsed_url._replace(query=""))
    return url_without_query

def sync_to_woocommerce(data, api_url, key, secret,excluded=True):
    """
    Sync product data to WooCommerce.
    """
    try:
        # Remove query from image URLs
        if excluded:
            for img in data['images']:
                img['src'] = remove_query_from_url(img['src'])

        # Initialize the WooCommerce API client
        wcapi = API(
            url=api_url,
            consumer_key=key,
            consumer_secret=secret,
            version="wc/v3",
            timeout=100
        )

        get_products=wcapi.get('products')
        res=get_products.json()
        
        # checking for already present products
        for products in res:
            if data['name'].lower() == products.get('name', '').lower():
                print('product already present')
                wcapi.put('products',data)
                print('data updated on store')
                return


        # Create product
        result = wcapi.post("products", data)
        if result.status_code == 201:
            print("Product successfully created!")
        else:
            print(f"Error: {result.status_code} - {result.text}")
    except Exception as e:
        print("Error in syncing to WooCommerce:", e)