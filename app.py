"""
Python MQTT Subscription client
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""
from flask import Flask, render_template
from w1thermsensor import W1ThermSensor
from flask_mqtt import Mqtt
from temppoint import TempPoint, temp_arr_to_string
import time
import random
from bs4 import BeautifulSoup
import requests

api_key = '2c24dbb46c5b9c9b615a1578321af2e9'
parameters = {
    'lat': 32.292647,
    'lon': 34.849826,
    'appid': api_key,
    'exclude': 'current,minutely,daily',
    'units': 'metric'
}


temp_livingr_sensor = 'HOLDER'

sensor = W1ThermSensor()
app = Flask(__name__)
# use the free broker from HIVEMQ
app.config['MQTT_BROKER_URL'] = '10.100.102.17'
app.config['MQTT_BROKER_PORT'] = 1884  # default port for non-tls connection
# set the username here if you need authentication for the broker
app.config['MQTT_USERNAME'] = 'yaron'
# set the password here if the broker demands authentication
app.config['MQTT_PASSWORD'] = 'yaron123'
# set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_KEEPALIVE'] = 5
# set TLS to disabled for testing purposes
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)

HOLDER = TempPoint(time.time(), 157)
rooms_arr = [[HOLDER], [HOLDER], [HOLDER], [HOLDER], [HOLDER]]
outside_temp_arr = []
outside_feels_like_arr = []
outside_arr = []
outside_chart_readys = ['', '']

OUTSIDE_TEMP = 0
OUTSIDE_FEELS = 1

LIVING_ROOM = 0
YARON_ROOM = 1
GUY_ROOM = 2
URIEL_ROOM = 3
PARENTS_ROOM = 4

# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message


def get_weather_info():
    response = requests.get(
        'https://api.openweathermap.org/data/2.5/onecall', params=parameters)

    current_temp = response.json()['hourly'][0]['temp']
    current_temp_feels_like = response.json()['hourly'][0]['feels_like']
    current_temp_description = response.json(
    )['hourly'][0]['weather'][0]['description']
    current_temp_humidity = response.json()['hourly'][0]['humidity']
    current_temp_wind_speed = response.json()['hourly'][0]['wind_speed']
    current_temp_dew_point = response.json()['hourly'][0]['dew_point']
    output = [current_temp, current_temp_feels_like, current_temp_description,
              current_temp_humidity, current_temp_wind_speed, current_temp_dew_point]
    return output


@mqtt.on_connect()
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print("Connected! ", str(rc))

    # Once the client has connected to the broker, subscribe to the topic
    mqtt.subscribe('req')
    mqtt.subscribe('temp0')
    mqtt.subscribe('temp2')
    mqtt.subscribe('temp3')
    mqtt.subscribe('temp4')


@mqtt.on_message()
def on_message(client, userdata, msg):
    global outside_temp_arr_ready, outside_feels_arr_ready
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    if msg.topic == 'req':
        room_index = YARON_ROOM
        temp_sensor = sensor.get_temperature()
        # OUTSIDE GRAPH
        weather_info = get_weather_info()
        current_time = time.time()
        temp_point = TempPoint(current_time, weather_info[0])
        temp_point_feels = TempPoint(current_time, weather_info[1])
        outside_temp_arr.append(temp_point)
        outside_feels_like_arr.append(temp_point_feels)
        if len(outside_temp_arr) >= 96:
            outside_temp_arr.pop(0)
        if len(outside_feels_like_arr) >= 96:
            outside_feels_like_arr.pop(0)
        outside_temp_arr_ready = temp_arr_to_string(outside_temp_arr)
        outside_feels_arr_ready = temp_arr_to_string(outside_feels_like_arr)

    else:
        room_index = int(msg.topic[-1])
        temp_sensor = str(msg.payload.decode())
    current_time = time.time()
    temp_point = TempPoint(current_time, temp_sensor)
    if len(rooms_arr[room_index]) >= 96:
        rooms_arr[room_index].pop(0)
    rooms_arr[room_index].append(temp_point)
    # if points_arr[room_index] is too long, remove first point from it
    print(str(msg.payload.decode()))

    #print ("Topic: ", msg.topic + "\nMessage: " + str(msg.payload.decode()))

    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

# debugging
# def request_temp():
#     mqtt.publish('req', 'REQUEST THE TEMP')


@app.route('/')
def index():
    global outside_arr, outside_chart_readys
    chart_readys = ['', '', '', '', '']
    for i in range(len(chart_readys)):
        chart_readys[i] = temp_arr_to_string(rooms_arr[i])
    last_time = rooms_arr[0][-1].time/1000
    current_time = int(time.time())
    next_refresh = 15*60-(current_time - last_time) + random.randint(1, 10)
    try:
        response = requests.get('http://10.100.102.50/')
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        all_temp = soup.find_all('span')
        global_temp = all_temp[0].text
        global_temp_c = global_temp[24:29]
        inside_temp = all_temp[1].text
        inside_temp_c = inside_temp[24:29]
        top_temp = all_temp[2].text
        top_temp_c = top_temp[21:26]
    except:
        pass
    weather_info = get_weather_info()
    return render_template('newIndex.html', refresh_interval=next_refresh, temp_yaron=rooms_arr[YARON_ROOM][-1].temp,
                           temp_livingr=rooms_arr[LIVING_ROOM][-1].temp, temp_guy=rooms_arr[GUY_ROOM][-1].temp, yaron_chart=(
                               chart_readys[YARON_ROOM]),
                           livingr_chart=(chart_readys[LIVING_ROOM]), guy_chart=(
                               chart_readys[GUY_ROOM]), GLOBAL_TEMP=global_temp_c,
                           INSIDE_TEMP=inside_temp_c, TOP_TEMP=top_temp_c, outside_temp=weather_info[
                               0], outside_feels_like=weather_info[1],
                           outside_descirption=weather_info[2], outside_humidity=weather_info[
                               3], outside_wind_speed=weather_info[4],
                           outside_dew_point=weather_info[5], outside_graph=outside_temp_arr_ready, outside_feels_graph=outside_feels_arr_ready)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=False)
    print('helloDear')
