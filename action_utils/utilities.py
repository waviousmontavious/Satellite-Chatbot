import os
import json
from rasa_sdk import Tracker


def get_dict(json_file):
    with open(json_file) as f:
        return json.load(f)


def get_last_bot_event(tracker: Tracker):
    event = next(e for e in reversed(tracker.events) if e['event'] == 'bot')
    return event['metadata']['template_name']
