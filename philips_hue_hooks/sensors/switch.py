from enum import unique, Enum

from philips_hue_hooks.device import Device


class Switch(Device):
    def __init__(self, sensor_id, sensor_name, sensor_category):
        super().__init__('sensor', sensor_id, sensor_name, sensor_category)
        self.state = None

    def update(self, json):
        state_from_json = json['state']['buttonevent']
        new_state = SwitchState(int(str(state_from_json)[0]))

        if self.state != new_state:
            self.state = new_state
            return new_state

        return None


@unique
class SwitchState(Enum):
    UNKNOWN = -1
    ON = 1
    BRIGHTNESS_UP = 2
    BRIGHTNESS_DOWN = 3
    OFF = 4

    @classmethod
    def _missing_(cls, value):
        return SwitchState.UNKNOWN
