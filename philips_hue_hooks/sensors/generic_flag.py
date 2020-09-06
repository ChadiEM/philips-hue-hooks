from philips_hue_hooks.device import Device


class GenericFlag(Device):
    def __init__(self, sensor_id, sensor_name, sensor_type):
        super().__init__('sensor', sensor_id, sensor_name, sensor_type)
        self.flag = None

    def update(self, json):
        flag_from_json = json['state']['flag']

        if self.flag != flag_from_json:
            self.flag = flag_from_json
            return flag_from_json

        return None
