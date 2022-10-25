import requests
import http.client
from urllib import parse


def send_data(statement, cid) :

    intent  = ''
    module_name = ''

    if 'intent' in statement.output['result'] :
        intent = statement.output['result']['intent'].strip()

    if 'module_title' in statement.output['result'] :
        module_name = statement.output['result']['module_title'].strip()


    if intent == '' :
        intent = "없음"
    if module_name == '' :
        module_name = "없음"

    if intent == 'root' :
        return

    params = {'v': '1', 't': 'pageview',
            'tid': 'UA-145267410-1',  'dh' : 'mrmind.ai', 'dp' : module_name, 'dt' : intent, 'cid' : cid}


    # print("===> checked : " , params)
    params = parse.urlencode(params)
    connection = http.client.HTTPSConnection('www.google-analytics.com')
    connection.request('POST', '/collect', params)

    response = connection.getresponse()
    # print(params)
    # print("GA response ====>", str(response.read()))

    connection.close()
