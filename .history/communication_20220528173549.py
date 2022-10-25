import requests
import json

def post(intent_list, intent_id, text):
    
    data = {
        "intent_list": intent_list,
        "intent_id": intent_id,
        "text": text
    }
    
    # URL = "http://192.168.0.44:8000/api/response"
    URL = "http://172.30.1.58:8000/api/response"
    headers = {'Content-Type': 'application/json; charset=utf-8'}
  
    res = requests.post(URL, data=json.dumps(data), headers=headers)
    _data = res.text
    
    if isinstance(_data, str):
        _data = json.loads(_data)
    
    return _data