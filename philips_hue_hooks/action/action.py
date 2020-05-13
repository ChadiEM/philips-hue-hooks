import abc


class Action:
    @abc.abstractmethod
    def invoke(self, device_class, device_id, device_type, new_state):
        pass
