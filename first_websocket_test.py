from websocket import create_connection
import time
import json



def build_message():
    # ws.send("Hello, World")
    message = system_control_message(
        system_control_component('system', 
            system_control_component(
                name='lodrive'

            ).__dict__
        ).__dict__
    )
    return message.__dict__

def build_message2():
    # ws.send("Hello, World")
    message = system_control_message(
        system_control_component('powersupply', 
            system_control_component(
                name='rack 1',
                command='get',
                variable='voltage',
                # value=10

            ).__dict__
        ).__dict__
    )
    return message.__dict__

#powersupply.rack 1.voltage?
#powersupply.rack 1.voltage 10

# while True:
try:
    options = dict()
    protocols = ['json_test, scpi_test']
    ws = create_connection("ws://localhost:80")#, subprotocols=protocols)
    # while True:

    ws.send('format= json')
    print ("Sent")
    print ("Receiving...")
    result =  ws.recv()
    print (f"Received '{result}'")
    
    print ("Sending 'Hello, World'...")
    message_object = build_message2()

    json_string = json.dumps(message_object, indent=2)
    ws.send(json_string)
    print ("Sent")
    print ("Receiving...")
    result =  ws.recv()

    print (f"Received '{result}'")
    time.sleep(1.00)
    # ws.send('goodbye')
    # result = ws.recv()
    # print (f"Received '{result}'")
finally:
    if ws:
        ws.close(status=1001)