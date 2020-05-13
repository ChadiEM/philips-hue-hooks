# Philips Hue Hooks

This is an experimental attempt to simulate a webhook behavior when motion is detected or when a light switch is pressed, by continuously polling the sensor status and sending a POST webhook when there is change.

**BETA alert**: APIs are subject to change!

## Sample Output (Logs)
```
... initialization omitted for brevity
[2020-05-13 17:07:39,953] INFO - sensor 5 (CLIPGenericStatus) => State.ON
[2020-05-13 17:07:39,953] INFO - light 3 (Extended color light) => LightState.ON
[2020-05-13 17:07:43,415] INFO - sensor 4 (ZLLSwitch) => SwitchState.OFF
[2020-05-13 17:07:43,415] INFO - sensor 5 (CLIPGenericStatus) => State.OFF
[2020-05-13 17:07:43,415] INFO - light 3 (Extended color light) => LightState.OFF
[2020-05-13 17:08:00,131] INFO - sensor 28 (CLIPGenericStatus) => State.OFF
[2020-05-13 17:08:00,131] INFO - light 1 (Dimmable light) => LightState.OFF
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

Build a hook target that listens to POST requests. The POST body will be:
```
{
    "class": <one of sensor/light>,
    "id": <sensor/light id>,
    "type": <device type>,
    "state": <new state>
}
```

where `new_state` is:
- for a motion detector: [on, off, turning_off]
- for a light switch: [on, brightness_up, brightness_down, off]
- for a light: [on, off]


Then start the motion poller:
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