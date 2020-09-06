from philips_hue_hooks.device import Device


class Presence(Device):
    def __init__(self, sensor_id, sensor_name, sensor_type):
        super().__init__('sensor', sensor_id, sensor_name, sensor_type)
        self.state = None

    def update(self, json):
        new_state = json['state']['presence']

        if self.state != new_state:
            self.state = new_state
            return new_state

        return None
