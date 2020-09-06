from philips_hue_hooks.device import Device


class NoopDevice(Device):
    def __init__(self):
        super().__init__('noclass', 0, 'noname', None)

    def update(self, json):
        return None
