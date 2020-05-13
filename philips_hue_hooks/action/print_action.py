import logging

from philips_hue_hooks.action.action import Action

LOG = logging.getLogger(__name__)


class LogAction(Action):
    def invoke(self, device_class, device_id, device_type, new_state):
        LOG.info(f'{device_class} {device_id} ({device_type}) => {new_state}')
