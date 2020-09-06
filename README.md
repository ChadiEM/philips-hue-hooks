# Philips Hue Hooks

This is an experimental attempt to simulate a hook behavior through continuously polling when any light or sensor changes state.

**BETA alert**: APIs are subject to change!

## Sample Output (Logs)
```
... initialization omitted for brevity
[2020-09-06 11:36:38,610] INFO - sensor 6 (Hue temperature sensor 1 / ZLLTemperature) => {'temperature': 2176, 'lastupdated': '2020-09-06T09:36:38'}
[2020-09-06 11:36:57,179] INFO - sensor 8 (Hue ambient light sensor 1 / ZLLLightLevel) => {'lightlevel': 19339, 'dark': False, 'daylight': False, 'lastupdated': '2020-09-06T09:36:56'}
[2020-09-06 11:37:06,472] INFO - sensor 8 (Hue ambient light sensor 1 / ZLLLightLevel) => {'lightlevel': 15107, 'dark': True, 'daylight': False, 'lastupdated': '2020-09-06T09:37:05'}
[2020-09-06 11:37:06,472] INFO - sensor 29 (textState / CLIPGenericStatus) => {'status': 0, 'lastupdated': '2020-09-06T09:37:05'}
[2020-09-06 11:40:03,068] INFO - sensor 7 (Entrance motion detector / ZLLPresence) => {'presence': True, 'lastupdated': '2020-09-06T09:40:02'}
[2020-09-06 11:40:03,068] INFO - sensor 28 (presenceState / CLIPGenericStatus) => {'status': 1, 'lastupdated': '2020-09-06T09:40:02'}
[2020-09-06 11:40:03,068] INFO - sensor 29 (textState / CLIPGenericStatus) => {'status': 0, 'lastupdated': '2020-09-06T09:40:02'}
[2020-09-06 11:40:03,068] INFO - light 1 (Entrance lamp / Dimmable light) => {'on': True, 'bri': 254, 'alert': 'select', 'mode': 'homeautomation', 'reachable': True}
[2020-09-06 11:40:07,715] INFO - sensor 8 (Hue ambient light sensor 1 / ZLLLightLevel) => {'lightlevel': 19299, 'dark': False, 'daylight': False, 'lastupdated': '2020-09-06T09:40:07'}
[2020-09-06 11:40:17,049] INFO - sensor 7 (Entrance motion detector / ZLLPresence) => {'presence': False, 'lastupdated': '2020-09-06T09:40:16'}
```

## Initialisation

### Identify the bridge address
```shell script
./discover.py
```

Or, alternatively, a network discovery tool such as `nmap`.

### Create a username
- Navigate to `http://<hostname>/debug/clip.html`
- POST `/api`, with body `{"devicetype":"insert_device_type_here"}`
- It will fail, press the button on the Hue hub and try again.
- It will succeed, and return a username. Copy it.

### Identify the sensors/lights (Optional)
- Navigate to `http://<hostname>/debug/clip.html`
- GET `/api/<username>/sensors`, and note the sensor ID corresponding to your motion detection sensor or light switch.

### More info
For more information, you can check Philips' [getting started](https://www.developers.meethue.com/documentation/getting-started) docs.

## Docker Quick Start
It will log notifications for all sensors and lights.
```
docker run -it --rm \
    -e BRIDGE_HOST=192.168.0.16 \
    -e USERNAME=DjKbc3uiIPf7xleIw08FD3UR7V1vzJGNnfRcDbFv \
      chadiem/philips-hue-hooks
```

## Run

### Test
```
./hook.sh --bridge-host=<host> \
    --username=<username>
```

For example,

```
./hook.sh --bridge-host=192.168.0.16 \
    --username=DjKbc3uiIPf7xleIw08FD3UR7V1vzJGNnfRcDbFv
```

Check that sensor movements are logged on stdout.

### Plug your webhook

#### Body Structure

Build a hook target that listens to POST requests. The POST body will be:
```
{
    "class": <one of sensor/light>,
    "id": <sensor/light id>,
    "type": <device type>,
    "state": <new state>
}
```

where `new_state` is a JSON body corresponding to the changed state.

#### Sample JSON bodies
```
{"class": "sensor", "id": "7", "name": "Entrance motion detector", "type": "ZLLPresence", "state": {"presence": false, "lastupdated": "2020-09-06T09:40:16"}}
{"class": "sensor", "id": "8", "name": "Hue ambient light sensor 1", "type": "ZLLLightLevel", "state": {"lightlevel": 12976, "dark": true, "daylight": false, "lastupdated": "2020-09-06T09:50:15"}}
{"class": "sensor", "id": "12", "name": "Virtual Button", "type": "CLIPGenericStatus", "state": {"status": 0, "lastupdated": "2020-09-03T22:28:48"}}
{"class": "sensor", "id": "15", "name": "Start and stop", "type": "CLIPGenericStatus", "state": {"status": 0, "lastupdated": "2020-09-03T22:28:53"}}
{"class": "sensor", "id": "28", "name": "presenceState", "type": "CLIPGenericStatus", "state": {"status": 0, "lastupdated": "2020-09-06T09:43:01"}}
{"class": "sensor", "id": "29", "name": "textState", "type": "CLIPGenericStatus", "state": {"status": 0, "lastupdated": "2020-09-06T09:45:16"}}
{"class": "light", "id": "1", "name": "Entrance lamp", "type": "Dimmable light", "state": {"on": false, "bri": 127, "alert": "select", "mode": "homeautomation", "reachable": true}}
{"class": "light", "id": "2", "name": "Bedroom lamp", "type": "Dimmable light", "state": {"on": false, "bri": 76, "alert": "select", "mode": "homeautomation", "reachable": true}}
{"class": "light", "id": "3", "name": "Living room main lamp", "type": "Extended color light", "state": {"on": false, "bri": 254, "hue": 0, "sat": 254, "effect": "none", "xy": [0.6915, 0.3083], "ct": 153, "alert": "select", "colormode": "xy", "mode": "homeautomation", "reachable": true}}
{"class": "sensor", "id": "7", "name": "Entrance motion detector", "type": "ZLLPresence", "state": {"presence": true, "lastupdated": "2020-09-06T09:52:49"}}
{"class": "light", "id": "1", "name": "Entrance lamp", "type": "Dimmable light", "state": {"on": true, "bri": 254, "alert": "select", "mode": "homeautomation", "reachable": true}}
{"class": "sensor", "id": "28", "name": "presenceState", "type": "CLIPGenericStatus", "state": {"status": 1, "lastupdated": "2020-09-06T09:52:49"}}
{"class": "sensor", "id": "29", "name": "textState", "type": "CLIPGenericStatus", "state": {"status": 0, "lastupdated": "2020-09-06T09:52:49"}}
{"class": "sensor", "id": "8", "name": "Hue ambient light sensor 1", "type": "ZLLLightLevel", "state": {"lightlevel": 18831, "dark": false, "daylight": false, "lastupdated": "2020-09-06T09:52:54"}}
```

#### Start the poller with a target webhook
```
./hook.sh --bridge-host=<host> \
    --username=<username> \
    --sensor-ids=<sensor_ids> \
    --target=<hook_target>
```

For example,

```
./hook.sh --bridge-host=192.168.0.16 \
    --username=DjKbc3uiIPf7xleIw08FD3UR7V1vzJGNnfRcDbFv \
    --sensor-ids=9 \
    --target=http://localhost:8080
```

