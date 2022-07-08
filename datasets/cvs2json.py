import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Union, Any


def csv_to_json(input_csv, output_json):
    result_json: List[Dict] = []
    result_dict: Dict[str, Union[Union[str, int], Dict]] = {}
    with open(input_csv, encoding='utf-8') as file_csv:
        # читаем  csv file  как список словарей
        csv_data = csv.DictReader(file_csv)
        for item in csv_data:
            if input_csv.split('.')[0] == 'ads':
                result_dict['model'] = "ads.Ads"
                result_dict['pk'] = item['id']
                result_dict['fields'] = {
                    "name": item['name'],
                    "author": item['author'],
                    "price": item['price'],
                    "description": item['description'],
                    "address": item['address'],
                    "is_published": item['is_published'],
                }
            if input_csv.split('.')[0] == 'categories':
                result_dict['model'] = "ads.Categories"
                result_dict['pk'] = item['id']
                result_dict['fields'] = {"name": item['name']}
            result_json.append(result_dict)

    with open(output_json, 'w', encoding='utf-8') as file_json:
        result = json.dumps(result_json, indent=4, ensure_ascii=False)
        file_json.write(result)


files = Path('.').glob('*.csv')
for file in files:
    csv_file = str(file)
    json_file = str(file).split('.csv')[0] + '.json'
    csv_to_json(csv_file, json_file)
