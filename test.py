import json

with open('test-config.json', 'r') as f:
    f_json = json.load(f)
    print('f_json: ', f_json)

