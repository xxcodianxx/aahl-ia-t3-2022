import csv
import json

def to_json():
    print('loading csv...')
    with open('../data/processed.csv', encoding='utf-8-sig') as f:
        rows = map(lambda x: x.strip().split(','), f.readlines())
        cols = rows.__next__()
        
        out = { col: [] for col in cols }

        for vals in rows:
            for i, v in enumerate(vals):
                out[cols[i]].append(float(v))

        return out

def read_data():
    print('loading data...')
    try:
        with open('../data/processed.json') as f:
            obj = json.load(f)
            return obj
    except FileNotFoundError:
        obj = to_json()
        print('creating json file...')
        with open('../data/processed.json', 'w+') as f:
            json.dump(obj, f, indent=4)
        return obj