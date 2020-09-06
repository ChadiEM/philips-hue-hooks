import logging
import time

import requests

from philips_hue_hooks.lights.light import Light
from philips_hue_hooks.noop_device import NoopDevice
from philips_hue_hooks.sensors.daylight import Daylight
from philips_hue_hooks.sensors.generic_flag import GenericFlag
from philips_hue_hooks.sensors.generic_status import GenericStatus
from philips_hue_hooks.sensors.lightlevel import LightLevel
from philips_hue_hooks.sensors.presence import Presence
from philips_hue_hooks.sensors.switch import Switch
from philips_hue_hooks.sensors.temperature import Temperature

LOG = logging.getLogger(__name__)


class Poller:
    def __init__(self, host, username, sensor_ids, light_ids, actions, poll_delay=0.5):
        self.host = host
        self.username = username
        self.sensor_ids = sensor_ids
        self.light_ids = light_ids
        self.actions = actions
        self.poll_delay = poll_delay

        self.devices = {}

    def run(self):
        while True:
            json = requests.get(f'http://{self.host}/api/{self.username}').json()

            if len(self.sensor_ids) == 0 and len(self.light_ids) == 0:
                self.sensor_ids = list(json['sensors'].keys())
                self.light_ids = list(json['lights'].keys())

            for sensor_id in self.sensor_ids:
                self.send_updates(json, 'sensor', sensor_id)
            for light_id in self.light_ids:
                self.send_updates(json, 'light', light_id)

            time.sleep(self.poll_delay)

    def send_updates(self, json, device_class, device_id):
        device_json = json[f'{device_class}s'][str(device_id)]

        device_key = f'{device_class}_{device_id}'

        current_device = self.devices.get(device_key)
        if current_device is None:
            current_device = self.create_device(device_class, device_id, device_json)
            self.devices[device_key] = current_device

        updated_state = current_device.update(device_json)

        if updated_state is not None:
            for action in self.actions:
                try:
                    action.invoke(current_device.get_device_class(),
                                  current_device.get_device_id(),
                                  current_device.get_device_name(),
                                  current_device.get_device_type(),
                                  updated_state)
                except Exception as exp:
                    LOG.warning('Unable to execute %s, error = %s', action, exp)

    @staticmethod
    def create_device(device_class, device_id, json):
        device_name = json['name']
        device_type = json['type']

        LOG.info(f'Initializing {device_class} {device_id} ({device_name} / {device_type})...')

        if device_type == 'Daylight':
            return Daylight(device_id, device_name, device_type)

        if device_type == 'CLIPGenericStatus':
            return GenericStatus(device_id, device_name, device_type)

        if device_type == 'CLIPGenericFlag':
            return GenericFlag(device_id, device_name, device_type)

        if device_type == 'ZLLSwitch':
            return Switch(device_id, device_name, device_type)

        if device_type == 'ZLLLightLevel':
            return LightLevel(device_id, device_name, device_type)

        if device_type == 'ZLLPresence':
            return Presence(device_id, device_name, device_type)

        if device_type == 'ZLLTemperature':
            return Temperature(device_id, device_name, device_type)

        if device_type == 'Dimmable light' or device_type == 'Extended color light':
            return Light(device_id, device_name, device_type)

        LOG.warning(f'Unable to listen to changes on {device_class} {device_id} ({device_name} / {device_type})')
        return NoopDevice()
