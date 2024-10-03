import time
import urllib.parse
from functools import lru_cache
from translator.translator import translate, Lang

import requests

# Base Url
base_url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601'

# Application ID
application_id = 'your_application_id'

# item info we needed
item_info_keys = ['itemName', 'itemPrice', 'itemUrl', 'mediumImageUrls', 'itemCode', 'reviewCount', 'catchcopy']

# retry counts
retry_counts = 5

# page_count_map
item_page_count = {}


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


def get_item_page_count(url):
    retry = 0
    while retry < retry_counts:
        response = requests.get(url)
        if response.status_code == 200:
            datas = response.json()

            if 'Items' in datas:
                return datas['pageCount']
            else:
                print("No items found")
            break
        else:
            print(f"Error code: {response.status_code}")
        time.sleep(0.5)
    return 0


def get_items_from_rakuten_api(keys, page):
    keys = translate(keys, Lang.EN, Lang.JA)[0]
    print(keys)
    keyword = urllib.parse.quote(keys, encoding='utf-8')
    sort = urllib.parse.quote('+reviewCount', encoding='utf-8')
    has_review_flag = urllib.parse.quote('1', encoding='utf-8')
    if keys not in item_page_count.keys():
        r_page = urllib.parse.quote('1', encoding='utf-8')
        url = f'{base_url}?applicationId={application_id}&keyword={keyword}&sort={sort}&page={r_page}&hasReviewFlag={has_review_flag}'
        item_page_count[keys] = get_item_page_count(url)
    r_page = urllib.parse.quote(str(item_page_count[keys] - page + 1), encoding='utf-8')
    url = f'{base_url}?applicationId={application_id}&keyword={keyword}&sort={sort}&page={r_page}&hasReviewFlag={has_review_flag}'
    return send_request_to_rakuten_ichiba_api(url)


@lru_cache(maxsize=128)
def get_item_from_rakuten_api(item_code):
    item_code = urllib.parse.quote(item_code, encoding='utf-8')
    url = f'{base_url}?applicationId={application_id}&itemCode={item_code}'
    return send_request_to_rakuten_ichiba_api(url)[0]


def calculate_similarity(items):
    for item in items:
        item['similarity'] = 0.0
    return items
