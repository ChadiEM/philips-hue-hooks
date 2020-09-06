from philips_hue_hooks.device import Device


class LightLevel(Device):
    def __init__(self, sensor_id, sensor_name, sensor_type):
        super().__init__('sensor', sensor_id, sensor_name, sensor_type)
        self.level = 0

    def update(self, json):
        level_from_json = json['state']['lightlevel']

        if self.level != level_from_json:
            self.level = level_from_json
            return level_from_json

        return None
