from enum import Enum, unique

from philips_hue_hooks.device import Device


class MotionSensor(Device):
    def __init__(self, sensor_id, sensor_type):
        super().__init__("sensor", sensor_id, sensor_type)
        self.state = None

    def update(self, json):
        state_from_json = json['state']['status']
        try:
            new_state = State(state_from_json)
        except ValueError:
            return "UNKNOWN_STATE"

        if self.state != new_state:
            self.state = new_state
            return new_state

        return None


@unique
class State(Enum):
    OFF = 0
    ON = 1
    TURNING_OFF = 2
