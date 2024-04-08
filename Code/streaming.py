import socketio
import json
import threading
import code_config
import time
import os
import sys

sio = socketio.Client()
token = code_config.INFOMAX_TOKEN

auth = {
    "token": token
}
packet = {
    "type": 'registCloseRealKey',
    "payload": ['CURR@EURUSD', 'CURR@USDJPY', 'STKITEM@069500', 'STKITEM@102110'],
    #"payload": ['STKITEM@069500', 'STKITEM@102110'],
}
namespace = '/svc-smartinfomax3'

@sio.on('DATA', namespace=namespace)
def catch_all(data):
    print("ping")
    #print("DATA=>", data)
    
    # Ensure the directory 'data' exists
    if not os.path.exists('D:/Projects/marketdata/RealTimeData'):
        os.makedirs('D:/Projects/marketdata/RealTimeData')

    # Save the data to a JSON file
    with open('D:/Projects/marketdata/RealTimeData/realtime.json', 'a') as f:
        json.dump(data, f)
        f.write(os.linesep)  # Write a newline at the end of each entry

sio.connect('http://smr.einfomax.co.kr', namespaces=namespace,auth=auth, wait_timeout=5, transports='websocket')
sio.emit('DATA', packet, namespace=namespace)
#sio.wait()
# Run sio.wait() in a separate thread
thread = threading.Thread(target=sio.wait)
thread.start()

try:
    # Wait for 30 seconds
    time.sleep(100)
except KeyboardInterrupt:
    print("Received KeyboardInterrupt, stopping threads.")

# Stop the connection
sio.disconnect()

# Wait for the thread to finish
thread.join()