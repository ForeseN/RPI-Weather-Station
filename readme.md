# RPi Weather Station
This is a Raspberry Pi project that runs a web server dashboard that shows the tempeature in every room.
![Alt text](readmeimage/homedashboard.png?raw=true "Optional Title")

# Why I built this?
Here's a funny story - My room is hotter than the rest of the house by a few degrees. Probably because The sun boils my walls all morning and the wall transfers the heat to the room throughout the day. For some reason my parents couldn't accept this and they said they don't feel a temperature difference.\
I had only one choice - Beat them with Technology, and what would be more exciting than writing the Technology yourself? (well kinda...)
anyways, a few weeks after writing the project, I've got myself an AC. Happy ending it is.

# How it works?
Basically, I put an Arduino board with a temperature sensor (DS18B20) in every room in my house.
I've used MQTT to transfer the weather data to my Raspberry Pi which collected every bit of data and put it in a nice graph made with JavaScript.\
In addition, I've used OpenWeatherAPI to get information about the weather outside aswell.
All the backend made with Flask.


# Required Components
Raspberry Pi - Runs the webserver and gets all the information from the Arduino's.\
Arduino (Each room + 1) - Sends the temperature data.\
DS18B20 (Each room + 1) - Temperature sensor.








