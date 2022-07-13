import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Union, Any


def csv_to_json(input_csv, output_json):
    result_json: List[Dict] = []
    result_dict: Dict[str, Union[Union[str, int], Dict]]
    temp_dict = defaultdict(lambda: 0)
    with open(input_csv, encoding='utf-8') as file_csv:
        # читаем  csv file  как список словарей
        csv_data = csv.DictReader(file_csv)
        for item in csv_data:
            result_dict = {}
            file_name: str = input_csv.split('.')[0]

            result_dict['model'] = f"{file_name}.{file_name.capitalize()}"
            result_dict['pk'] = item['id']

            fields = [field_name for field_name in item.keys() if field_name != 'id']

            for field in fields:
                temp_dict[f"{field}"] = item[f"{field}"]

            result_dict['fields'] = temp_dict

            result_json.append(result_dict)

    with open(output_json, 'w', encoding='utf-8') as file_json:
        result = json.dumps(result_json, indent=4, ensure_ascii=False)
        file_json.write(result)


files = Path('.').glob('*.csv')
for file in files:
    csv_file = str(file)
    json_file = str(file).split('.csv')[0] + '.json'
    csv_to_json(csv_file, json_file)
