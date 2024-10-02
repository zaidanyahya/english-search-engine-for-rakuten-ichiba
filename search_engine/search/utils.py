import time
import urllib.parse
from functools import lru_cache

import requests

# Base Url
base_url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601'

# Application ID
application_id = 'your_application_id'

# item info we needed
item_info_keys = ['itemName', 'itemPrice', 'itemUrl', 'mediumImageUrls', 'itemCode']

# retry counts
retry_counts = 5


def send_request_to_rakuten_ichiba_api(url):
    items = []
    retry = 0
    while retry < retry_counts:
        response = requests.get(url)
        if response.status_code == 200:
            datas = response.json()

            if 'Items' in datas:
                for data in datas['Items']:
                    item_info = data['Item']
                    item = {}
                    for item_info_key in item_info_keys:
                        item[item_info_key] = item_info[item_info_key]
                        # print(f"{item_info_key}: {item_info[item_info_key]}")
                    items.append(item)
                    # print()
            else:
                print("Not found")
            break
        else:
            print(f"Error code: {response.status_code}")
        time.sleep(0.5)
    return items


def get_items_from_rakuten_api(keys, page):
    keyword = urllib.parse.quote(keys, encoding='utf-8')
    sort = urllib.parse.quote('+reviewAverage', encoding='utf-8')
    page = urllib.parse.quote(str(page), encoding='utf-8')
    url = f'{base_url}?applicationId={application_id}&keyword={keyword}&sort={sort}&page={page}'
    return send_request_to_rakuten_ichiba_api(url)


@lru_cache(maxsize=128)
def get_item_from_rakuten_api(item_code):
    item_code = urllib.parse.quote(item_code, encoding='utf-8')
    url = f'{base_url}?applicationId={application_id}&itemCode={item_code}'
    return send_request_to_rakuten_ichiba_api(url)[0]
