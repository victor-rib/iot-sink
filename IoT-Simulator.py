from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
from os import walk
from datetime import datetime, timedelta


ENDPOINT = "a38l0zpw6zq93h-ats.iot.sa-east-1.amazonaws.com"
BASE_PATH = "C:\\Users\\" # Certificates Path
PATH_TO_AMAZON_ROOT_CA_1 = BASE_PATH+"certificates\\AmazonRootCA1.pem"
TOPIC = "sensors/tanklevel"
RANGE = 20

currenttime = datetime.now()
filenames = next(walk(BASE_PATH+"certificates"), (None, None, []))[2]
devicelist = []

for file in filenames:
    if ("_certificate.pem" in file):
        devicelist.append(file.replace('_certificate.pem',''))


print(devicelist)

'''
filtered = []
for device in devicelist:
    if(device == 'device21'):
        filtered.append(device)
devicelist = filtered
print(devicelist)
'''

for device in devicelist:
    CLIENT_ID = device
    PATH_TO_CERTIFICATE = BASE_PATH+"certificates\\"+device+"_certificate.pem"
    PATH_TO_PRIVATE_KEY = BASE_PATH+"certificates\\private_"+device+".key"
    
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
                endpoint=ENDPOINT,
                cert_filepath=PATH_TO_CERTIFICATE,
                pri_key_filepath=PATH_TO_PRIVATE_KEY,
                client_bootstrap=client_bootstrap,
                ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
                client_id=CLIENT_ID,
                clean_session=False,
                keep_alive_secs=6
                )
    print("Connecting to {} with client ID '{}'...".format(
            ENDPOINT, CLIENT_ID))
    # Make the connect() call
    connect_future = mqtt_connection.connect()
    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")
    # Publish message to server desired number of times.
    print('Begin Publish')
    
    for x in range(RANGE):
      devNumber = int(device.replace('device',''))
      group = 'group-2' if devNumber % 2 == 0 else 'group-1'
      measuretime = str(currenttime + timedelta(minutes=x*(60/RANGE)))
      message = {"value" : 100-2*x, "voltage": 5, "temperature": 25 ,"deviceid": CLIENT_ID, "provider" : "providerX", "group": group, "timestamp" : measuretime}
      if(devNumber == 16 or devNumber == 32  or devNumber == 8  or devNumber == 24):
            message['voltage'] = message['voltage'] - x
            message['voltage'] = 0 if message['voltage'] < 0 else message['voltage']
      elif(devNumber == 5 or devNumber == 10 or devNumber == 25 or devNumber == 15 or devNumber == 20):
            message['temperature'] = message['temperature'] + x * 10
      elif(devNumber == 21 or devNumber == 7 or devNumber == 14):
            message['value'] = message['value'] - x * 100
            message['value'] = 0 if message['value'] < 0 else message['value']

      mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
      print("Published: '" + json.dumps(message) + "' to the topic: " + "'test/testing'")
      t.sleep(0.1)
    
    print('Publish End')
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
