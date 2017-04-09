from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent
import paho.mqtt.client as mqtt
import configparser
import logging
import time
import signal
import sys

config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(filename='example.log',level=logging.INFO)

def signal_handler(signal, frame):
    print('Ctrl-C received. Program exiting')
    print('Cleaning up')
    #client.loop_stop()
    sys.exit(0)

####### Register handler for SIGINT graceful exit ######
signal.signal(signal.SIGINT, signal_handler)

####### Telegram - create updater and link it to bot, then dispatcher  #######
updater = Updater(token=config['KEYS']['bot_token'])
dispatcher = updater.dispatcher

######## Start of MQTT Functionality ############
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe(config['MQTT_SERVER']['mqtt_feed'])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(time.strftime('%H:%M:%S')+" "+msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.username_pw_set(config['ADAFRUIT']['user_name'], password=config['ADAFRUIT']['api_token'])
client.on_connect = on_connect
client.on_message = on_message

client.connect(config['MQTT_SERVER']['mqtt_url'], 1883, 60)
client.loop_start()



# Infinite loop to keep program executing while multithreaded components carry on
while True:
    pass

# Code snippets to keep
'''for x in range(1,10):
    time.sleep(1) #Note that this does not block the MQTT loop at all. Yay!
    print x'''
