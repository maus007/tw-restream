# -*- coding: utf-8 -*-

import apiai, json


def textMessage(msg):
    request = apiai.ApiAI('a16df32cc5544b8a8634d95070c57479').text_request()
    request.lang = 'ru' 
    request.session_id = 'genius_fortnite_player'
    request.query = msg
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if response:
        return response


