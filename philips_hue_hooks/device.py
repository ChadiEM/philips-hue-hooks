import abc


class Device:
    def __init__(self, device_class, device_id, device_name, device_type):
        self._device_class = device_class
        self._device_id = device_id
        self._device_name = device_name
        self._device_type = device_type

    def get_device_class(self):
        return self._device_class

    def get_device_id(self):
        return self._device_id

    def get_device_name(self):
        return self._device_name

    def get_device_type(self):
        return self._device_type

    @abc.abstractmethod
    def update(self, json):
        pass
