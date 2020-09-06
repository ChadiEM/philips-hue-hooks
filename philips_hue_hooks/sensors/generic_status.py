from philips_hue_hooks.device import Device


class GenericStatus(Device):
    def __init__(self, sensor_id, sensor_name, sensor_type):
        super().__init__('sensor', sensor_id, sensor_name, sensor_type)
        self.state = None

    def update(self, json):
        status_from_json = json['state']['status']

        if self.state != status_from_json:
            self.state = status_from_json
            return status_from_json

        return None
