import requests


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def lookup_urban(search_term):
    url = 'http://api.urbandictionary.com/v0/define'
    params = {
        'term': search_term,
    }
    r = requests.get(url, params=params, timeout=3)
    j = r.json()
    return j['list'][0]['definition']


def lambda_handler(event, context):
    print('event: {}'.format(event))

    try:
        value = event['request']['intent']['slots']['term']['value']
        value = value.lower().replace('define', '').strip()
        value = value.lower().replace('lookup', '').strip()
        value = value.lower().replace('look up', '').strip()
        value = value.lower().replace('search', '').strip()
        value = value.lower().replace('find', '').strip()
        print('value: {}'.format(value))
    except Exception as error:
        print('error: {}'.format(error))
        resp = 'I did not understand that request, please try something else.'
        alexa = build_response(
            {},
            build_speechlet_response('Error', resp, None, True)
        )
        return alexa

    try:
        definition = lookup_urban(value)
        print('definition: {}'.format(definition))
        resp = '{}. {}'.format(
            value, definition
        )
        alexa = build_response(
            {},
            build_speechlet_response('Definition', resp, None, True)
        )
        return alexa
    except Exception as error:
        print('error: {}'.format(error))
        resp = 'Error looking up {}, please try something else.'.format(value)
        alexa = build_response(
            {},
            build_speechlet_response('Error', resp, None, True)
        )
        return alexa

