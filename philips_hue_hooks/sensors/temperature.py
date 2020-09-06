from philips_hue_hooks.device import Device


class Temperature(Device):
    def __init__(self, sensor_id, sensor_name, sensor_type):
        super().__init__('sensor', sensor_id, sensor_name, sensor_type)
        self.temperature = 0.0

    def update(self, json):
        state_from_json = json['state']['temperature']
        updated_temp = state_from_json / 100

        if self.temperature != updated_temp:
            self.temperature = updated_temp
            return updated_temp

        return None
