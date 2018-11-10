import logging

from philips_hue_hooks.action.action import Action

LOG = logging.getLogger(__name__)


class LogAction(Action):
    def invoke(self, sensor_id, new_state):
        LOG.info(f'Sensor {sensor_id} => {new_state}')
