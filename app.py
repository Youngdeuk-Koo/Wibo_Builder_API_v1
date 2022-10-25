from flask import request
from flask_api import FlaskAPI, status
from chatterbot import ChatBot
from chatterbot import utils

import datetime as dt
import json
import logging
import settings

utils.event_log('event')

app = FlaskAPI(__name__)


@app.route("/api/<chatbot_id>/<user_key>", methods=['GET', 'POST'])
def api2(chatbot_id, user_key):

    # initial message
    if request.method == 'GET':

        chatbot = ChatBot(chatbot_id=chatbot_id, user_key=user_key, **settings.CHATBOT)
        response = chatbot.get_init_response()
        return json.dumps(response, ensure_ascii=False), status.HTTP_200_OK

    # chat message
    if request.method == 'POST':                                                          

        chatbot = ChatBot(chatbot_id=chatbot_id, user_key=user_key, **settings.CHATBOT) 
        _data = request.data                                                                     
        if isinstance(_data, str):                                                                 
            _data = json.loads(_data) 

        response = chatbot.get_response(_data)                                                         
        return json.dumps(response, ensure_ascii=False), status.HTTP_200_OK


if __name__ == '__main__':
    default_host = "0.0.0.0"
    default_port = "10732"

    import os
    os.environ['FLASK_ENV'] = "development"

    import optparse
    parser = optparse.OptionParser()

    parser.add_option("-H", "--host",
                      help="Hostname of the Flask app " + \
                           "[default %s]" % default_host,
                      default=default_host)

    parser.add_option("-P", "--port",
                      help="Port for the Flask app " + \
                           "[default %s]" % default_port,
                      default=default_port)

    options, _ = parser.parse_args()

    app.run(
        debug=True,
        host=options.host,
        port=int(options.port)
    )
