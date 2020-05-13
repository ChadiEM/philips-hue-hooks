import requests

from philips_hue_hooks.action.action import Action


class WebHookAction(Action):
    def __init__(self, post_url):
        self.post_url = post_url

    def __str__(self):
        return f'WebHook at {self.post_url}'

    def invoke(self, device_class, device_id, device_type, new_state):
        state = new_state.name.lower()

        requests.post(self.post_url, json={
            'class': device_class,
            'id': device_id,
            'type': device_type,
            'state': state
        })
