import random
import json
#import urllib2
import urllib3
import shelve

import temp_humidity
import led
import time

topics = None

COMMAND1 = "who are you"
COMMAND2 = "what can you do"
COMMAND3 = "temp"
#COMMAND4 = "name an animal"
#COMMAND5 = "green led"
COMMAND4 = "topic:"
COMMAND5 = "topics"
COMMAND6 = "get-ip"

headers =  { 'x-api-key': 'rbfYSjUHLS58VdblPBdAZ6sUYiAhJhOe1hCTUKGc',
                 'Content-Type': 'application/json' }


def blink_green():
    for i in range(2):
        time.sleep(0.2)
        led.green_led(1)
        time.sleep(0.2)
        led.green_led(0)

def blink_red():
    for i in range(2):
        time.sleep(0.2)
        led.red_led(1)
        time.sleep(0.2)
        led.red_led(0)
    
def open():
    pass
    #return shelve.open('topics')

def save_topic(topic, source ="", user=""):
    data = { "topic" : topic,
             "source" : source,
             "user" : user }
    #request = urllib2.Request('https://ogdpk9s2k8.execute-api.us-east-1.amazonaws.com/prod/topicCrud',json.dumps(data),headers)
    #response = urllib2.urlopen(request)

    http = urllib3.PoolManager()
    response = http.urlopen('POST','https://ogdpk9s2k8.execute-api.us-east-1.amazonaws.com/prod/topicCrud', headers=headers, body=json.dumps(data)).data
    return response

def all_topics():
    global topics
    http = urllib3.PoolManager()
    response = http.urlopen('GET','https://ogdpk9s2k8.execute-api.us-east-1.amazonaws.com/prod/topicCrud', headers=headers).data
    topics = json.loads(response)
    print topics
    return response

def tag_scanner(bot_id,output):
    global topics
    if not topics:
        all_topics()
    for word in output['text'].split(" "):
        if word.lower() in topics.keys():
            source = "slack #" + bot_id.get_channel_name(output['channel'])
            user = bot_id.get_user_name(output['user'])
            save_topic(word,source,user)
            blink_green()
        #elif 'tccmd.wrayesian.com' in word:
        #    blink_red()
        
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

    elif command.find(COMMAND6) >= 0:
        import socket
        response = str(socket.gethostbyname(socket.gethostname()))


    return response

