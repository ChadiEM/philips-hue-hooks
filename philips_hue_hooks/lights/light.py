from enum import Enum, unique

from philips_hue_hooks.device import Device


class Light(Device):
    def __init__(self, light_id, light_type):
        super().__init__("light", light_id, light_type)
        self.state = None

    def update(self, json):
        state_from_json = json['state']['on']
        new_state = LightState(state_from_json)

        if self.state != new_state:
            self.state = new_state
            return new_state

        return None


@unique
class LightState(Enum):
    ON = True
    OFF = False
