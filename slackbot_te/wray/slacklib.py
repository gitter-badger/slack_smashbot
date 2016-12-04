import random
import json
#import urllib2
import urllib3
import shelve

import temp_humidity
#import led

topics = []

COMMAND1 = "who are you"
COMMAND2 = "what can you do"
COMMAND3 = "temp"
#COMMAND4 = "name an animal"
#COMMAND5 = "green led"
COMMAND4 = "topic:"
COMMAND5 = "topics"

headers =  { 'x-api-key': 'rbfYSjUHLS58VdblPBdAZ6sUYiAhJhOe1hCTUKGc',
                 'Content-Type': 'application/json' }

def open():
    pass
    #return shelve.open('topics')

def save_topic(topic):
    data = { "topic" : topic }
    #request = urllib2.Request('https://ogdpk9s2k8.execute-api.us-east-1.amazonaws.com/prod/topicCrud',json.dumps(data),headers)
    #response = urllib2.urlopen(request)

    http = urllib3.PoolManager()
    response = http.urlopen('POST','https://ogdpk9s2k8.execute-api.us-east-1.amazonaws.com/prod/topicCrud', headers=headers, body=json.dumps(data)).data
    return response

def all_topics():
    http = urllib3.PoolManager()
    response = http.urlopen('GET','https://ogdpk9s2k8.execute-api.us-east-1.amazonaws.com/prod/topicCrud', headers=headers).data
    topics = json.loads(response)
    return response

def tag_scanner(output):
    for word in output['text']:
        if word in topics.keys():
            save_topic(word)
        
def handle_command(command):
    """
        Determine if the command is valid. If so, take action and return
        a response, if necessary.
    """
    response = ""
    if command.find(COMMAND1) >= 0:
        response = "I am a simpleton bot."
    elif command.find(COMMAND2) >= 0:
        response = "Not much right now... waiting for you to teach me."
    elif command.find(COMMAND3) >= 0:
        try:
            temp_c,temp,humidity = temp_humidity.read_temp_humidity()
            response = "At my location, the temperature is " + str(temp) + " and the relative humidity is " + str(humidity)
        except:
            response = "At my location, there is a sensor malfunction."

    elif command.find(COMMAND4) >= 0:
        command = command.encode('utf-8')
        ti = command.find(':')
        topic = command[ti+1:].strip()
        response = save_topic(topic)
        #response = (ret + " added.") if ret else (topic + " already in there.")
        

    elif command.find(COMMAND5) >= 0:
        response = all_topics()
        


    return response

