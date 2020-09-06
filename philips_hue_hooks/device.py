class Device:
    def __init__(self, device_class, device_id, device_name, device_type):
        self._device_class = device_class
        self._device_id = device_id
        self._device_name = device_name
        self._device_type = device_type
        self._state = None

    def get_device_class(self):
        return self._device_class

    def get_device_id(self):
        return self._device_id

    def get_device_name(self):
        return self._device_name

    def get_device_type(self):
        return self._device_type

    def update(self, json):
        new_state = json['state']

        if self._state != new_state:
            self._state = new_state
            return new_state

        return None
