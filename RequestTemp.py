import paho.mqtt.client as mqtt  # Import the MQTT library

import time  # The time library is useful for delays


# Our "on message" event

def messageFunction(client, userdata, message):

    topic = str(message.topic)

    message = str(message.payload.decode("utf-8"))

    print(topic + message)


ourClient = mqtt.Client("makerio_mqtt")  # Create a MQTT client object

ourClient.connect("10.100.102.17", 1884)  # Connect to the test MQTT broker

ourClient.subscribe("req")  # Subscribe to the topic AC_unit

# Attach the messageFunction to subscription
ourClient.on_message = messageFunction

ourClient.loop_start()  # Start the MQTT client


# Main program loop

while(1):

    # Publish message to MQTT broker
    ourClient.publish("req", "REQUEST THE TEMP")

    # Sleep for 15 min and then publishes again / asks for temp from all the devices
    time.sleep(300)
    print("10 min left")
    time.sleep(300)
    print("5 min left")
    time.sleep(300)
