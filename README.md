# Smart-Car-Park

## Setup Instructions
GrovePi requires a Raspberry Pi with Raspberry Pi OS installed.
In my experience, only the 32-bit legacy version of Raspberry Pi OS works with GrovePi.
The installation script also requires a user with the name `pi` and sudo privileges.

```curl -kL dexterindustries.com/update_grovepi | bash```

The PDDL planner used in this project is `pyperplan`.
To install it, run:

```pip install pyperplan```

and set the PATH variable to include the directory where `pyperplan` is installed:

```echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc source ~/.bashrc```

For the messaging system, this project uses Twilio.
To install the Twilio Python library, run:

```pip install twilio```
```pip install python-dotenv```

Then go to [Twilio](https://www.twilio.com/) and create an account.
Then set the environment variables `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` int the .env file.

Install the mosquitto MQTT broker on the Raspberry Pi:

```sudo apt install mosquitto```
and enable it to start on boot:

```sudo systemctl enable mosquitto```

then add 

listener 1883
allow_anonymous true

To the `/etc/mosquitto/mosquitto.conf` file.

To use the LED strip, you need to install the `neopixel` library.
```pip3 install adafruit-circuitpython-neopixel```
This library requires root privileges to run.