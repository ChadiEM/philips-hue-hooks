from enum import Enum, unique

from philips_hue_hooks.device import Device


class MotionSensor(Device):
    def __init__(self, sensor_id, sensor_type):
        super().__init__("sensor", sensor_id, sensor_type)
        self.state = None

    def update(self, json):
        state_from_json = json['state']['status']
        new_state = State(state_from_json)

        if self.state != new_state:
            self.state = new_state
            return new_state

        return None


@unique
class State(Enum):
    UNKNOWN = -1
    OFF = 0
    ON = 1
    TURNING_OFF = 2

    @classmethod
    def _missing_(cls, value):
        return State.UNKNOWN
