import requests
from Scraper.pushData import sync_to_woocommerce

class TemuScraper:
    def __init__(self, keys, api_sec, apikey, api_url):
        self.keywords = keys
        self.apisec = api_sec
        self.api_key = apikey
        self.apiurl = api_url
        self.products = []    

    def scrape_data_from_api(self, url):
        try:    
            Title = None
            Description = None
            prices = None
            stock_status = 'outofstock'
            product_url = None
            images = []
            # Add headers if the API expects a specific user-agent
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            }
            # Proxy dictionary
            proxies = {
                "http": "http://odyuipwr-rotate:o3aagt6vgwds@p.webshare.io:80",
                "https": "http://odyuipwr-rotate:o3aagt6vgwds@p.webshare.io:80",
            }
            res = requests.get(url, headers=headers, proxies=proxies)
            res.raise_for_status()
            data = res.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return

        for item in data.get('result', {}).get('home_goods_list', []):
            for key in self.keywords:
                if key in item.get('data', {}).get('title', ''):
                    video_data = item.get('data', {}).get('video', {})
                    # Check if video data exists and then format images array
                    for value in video_data.values():
                        if not value.endswith('.mp4'):
                         images.append({'src':value})

                    # Extract title, description, and price info
                    Title = item.get('data', {}).get('title', '')
                    Description = item.get('data', {}).get('page_alt', '')
                    prices = item.get('data', {}).get('price_info', {}).get('price_str', 'Not Available')

                    # Determine stock status based on 'sales_num'
                    sales_num = item.get('data', {}).get('sales_num', '0')
                    stock_status = 'instock' if 'K' in sales_num or int(sales_num.replace('K', '').replace('+', '').strip()) > 0 else 'outofstock'

                    # Extract product URL
                    product_url = item.get('data', {}).get('link_url', '')

                    if len(images) > 0 and Title and Description and prices and stock_status:
                        product_data = {
                            "name": Title,  # Product title
                            "description": Description,  # Product description
                            "regular_price": prices,  # Product price
                            "stock_status": stock_status,  # Stock status ('instock' or 'outofstock')
                            "product_url": product_url,  # Product URL
                            "images": images,  # Image URLs
                        }
                        sync_to_woocommerce(product_data, self.apiurl, self.api_key, self.apisec)



offset_array = [i for i in range(0, 200000, 20)]

def Temu(keys, api_sec, apikey, api_url):
      Scraper=TemuScraper(keys, api_sec, apikey, api_url)
      print('scraper started')
      for offset in offset_array:
            url=f'https://www.temu.com/api/alexa/homepage/goods_list?offset={offset}&count=20&list_id=a693d17197a34589af44e095ca72b3fd&opt_id=&opt_type=&filter_items=&scene=home&page_list_id=393cff2948a44548b437acba06504f36&page_sn=10005&page_el_sn=201803'
            Scraper.scrape_data_from_api(url)