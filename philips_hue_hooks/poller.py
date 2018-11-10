import logging
import time

import requests

from philips_hue_hooks.sensors.motion_sensor import MotionSensor
from philips_hue_hooks.sensors.switch import Switch

LOG = logging.getLogger(__name__)


def create_sensor(sensor_id, json):
    if json['type'] == 'CLIPGenericStatus':
        return MotionSensor(sensor_id)

    if json['type'] == 'ZLLSwitch':
        return Switch(sensor_id)

    raise ValueError('Unable to listen to changes on this sensor')


class Poller:
    def __init__(self, host, username, sensor_ids, actions, poll_delay=0.5):
        self.host = host
        self.username = username
        self.sensor_ids = sensor_ids
        self.actions = actions
        self.poll_delay = poll_delay

        self.sensors = {}

    def run(self):
        while True:
            json = requests.get(f'http://{self.host}/api/{self.username}/sensors').json()

            for sensor_id in self.sensor_ids:
                sensor_json = json[str(sensor_id)]

                current_sensor = self.sensors.get(sensor_id)
                if current_sensor is None:
                    current_sensor = create_sensor(sensor_id, sensor_json)
                    self.sensors[sensor_id] = current_sensor

                updated_state = current_sensor.update(sensor_json)

                if updated_state is not None:
                    for action in self.actions:
                        try:
                            action.invoke(current_sensor.get_sensor_id(), updated_state)
                        except Exception as exp:
                            LOG.warning('Unable to execute %s, error = %s', action, exp)

            time.sleep(self.poll_delay)
