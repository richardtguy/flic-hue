# flic-hue
Use flic Bluetooth buttons to control Philips hue lights via a Raspberry Pi 3.

## Overview
- This application enables flic bluetooth LE buttons to be used to control Philips hue smart lights via a Raspberry Pi 3 running Rasbian.

- Verified buttons communicates with the Bluetooth controller on the Raspberry Pi via a server application which serves click events to a client application.  The client queries the hue bridge API to switch lights on or off depending on the click type (single click or hold).  Buttons are associated with groups of lights as defined in a JSON formatted file.

## Instructions
- In one terminal, start flic server (as root)
```
cd server
sudo ./flicd -f flic.sqlite3
```

- To connect new buttons, in another terminal, `cd simpleclient`, compile it with `make` and run with `./simpleclient localhost`. You will be shown the available commands. Type `startScan` and press enter to start scanning for buttons. Then press your flic button (and make sure it is disconnected to any other devices such as a smartphone) and you should see it appear. Type `stopScan` and press enter to stop scanning (it's ok if output text are interleaved with what you type). Hold your Flic button for 7 seconds to make it public, and make sure that it glows red. Then enter the command connect `<BDADDR> <id>` where `<BDADDR>` is the address that appeared during scan. For `<id>`, put any integer that will be used later to refer to this connection. The button should now connect and you will see click events appear. Type `disconnect <id>` to later disconnect.

- To run the light switch client, `cd client` and run with `./my_client.py`

- Press and hold any button to switch off all lights

- To turn on a group of lights when a button is single-clicked, add the button and a list of light IDs to the 'groups' file.  Light IDs can be obtained by querying the /lights resource on the hue bridge.
```
{
    "80:e4:da:71:36:f6": {
        "group": [
            4,
            5,
            6
        ]
    }
}
```

## References
- flic button server & client libraries: `https://github.com/50ButtonsEach/fliclib-linux-hci`
- Philips hue API: `http://www.developers.meethue.com/philips-hue-api`
- Python library for Philips hue: `https://github.com/quentinsf/qhue`

