import logging

import configargparse

from philips_hue_hooks.action.print_action import LogAction
from philips_hue_hooks.action.webhook_action import WebHookAction
from philips_hue_hooks.discovery.hue_discovery import NetworkBridgeDiscovery
from philips_hue_hooks.poller import Poller

LOG = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = configargparse.ArgParser(description='Hook Arguments')

    parser.add('--bridge-host',
               env_var='BRIDGE_HOST',
               help='Hostname/IP address to poll on (for example: 192.168.0.17)')
    parser.add('--username',
               required=True,
               env_var='USERNAME',
               help='Username to use (for example: DjKbc3uiIBf7xleIw08FD3UR7V1vzJGNnfRcDbFv)')
    parser.add('--sensor-ids',
               required=True,
               env_var='SENSOR_IDS',
               help='Comma-separated list of sensor IDs (for example: 4,9)')
    parser.add('--target',
               action='append',
               env_var='TARGET',
               help='The WebHook URL(s) to POST to (optional; if absent, will print to stdout)')

    args = parser.parse_known_args()[0]

    username = args.username
    sensor_id = [int(i) for i in args.sensor_ids.split(',')]

    actions = []

    host = args.bridge_host
    if host is None:
        LOG.info("No bridge host provided.")

        host = NetworkBridgeDiscovery().discover()

        if host is None:
            raise ValueError('Unable to find Hue bridge host')

    if args.target is None:
        actions.append(LogAction())
    else:
        for target in args.target:
            actions.append(WebHookAction(target))

    poller = Poller(host, username, sensor_id, actions)
    poller.run()
