import logging.config

from netdisco.discovery import NetworkDiscovery

from philips_hue_hooks.discovery.discovery import Discovery

LOG = logging.getLogger(__name__)


class NetworkBridgeDiscovery(Discovery):

    def discover(self):
        hue_devices = []

        LOG.info('Searching for a Hue device...')

        netdis = NetworkDiscovery()
        netdis.scan()

        for dev in netdis.discover():
            for info in netdis.get_info(dev):
                if 'name' in info and 'Philips hue' in info['name']:
                    hue_devices.append(info)
                    LOG.info('Hue device found: %s', info['host'])

        netdis.stop()

        if len(hue_devices) == 1:
            return hue_devices[0]['host']

        if len(hue_devices) == 2:
            LOG.warning('More than one Hue device found.')
        elif not hue_devices:
            LOG.warning('No Hue devices found.')

        return None
