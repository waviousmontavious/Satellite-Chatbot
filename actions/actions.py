from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset

from action_utils import get_dict, get_last_bot_event, get_weather


fid_db = get_dict('./fid-dictionary.json')  # failure id dictionary
sensor_db = get_dict('./sensor-dictionary.json')  # sensor dictionary


# Failure Form Validator ----------------------------------------------------------------------------------------------
class FailureForm(FormValidationAction):

    activation_intent = 'something_wrong'  # user intent that activates this form

    # The name of this Action
    def name(self) -> Text:
        return "validate_failure_form"

    # The required_slots() function updates the form with slots that have a custom extraction method
    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        custom_slots = ['user_received_alert', 'user_receiving_data']
        return custom_slots + slots_mapped_in_domain

    # Extraction function for the 'user_received_alert' slot
    async def extract_user_received_alert(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict,
    ) -> Dict[Text, Any]:
        # Return an empty dictionary if the bot isn't asking to fill the slot
        if tracker.get_intent_of_latest_message() == self.activation_intent:
            return {}
        if get_last_bot_event(tracker) != 'utter_ask_user_received_alert':
            return {}

        # Set the alert and data slots to true if the user confirms they have an alert
        if tracker.get_intent_of_latest_message() == 'user_confirm':
            return {"user_received_alert": True, "user_receiving_data": True}
        elif tracker.get_intent_of_latest_message() == 'user_deny':
            return {"user_received_alert": False, "user_receiving_data": None}
        else:
            dispatcher.utter_template('utter_doesnt_answer', tracker)
            return {}

    # Extraction function for the 'user_receiving_data' slot
    async def extract_user_receiving_data(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict,
    ) -> Dict[Text, Any]:
        # Return an empty dictionary if the bot isn't asking to fill the slot
        if tracker.get_intent_of_latest_message() == self.activation_intent:
            return {}
        if get_last_bot_event(tracker) != 'utter_ask_user_receiving_data':
            return {}

        # Set the data to true if the user is receiving data and reset the alert slot so the bot requests it again
        if tracker.get_intent_of_latest_message() == 'user_confirm':
            dispatcher.utter_template('utter_check_for_fid', tracker)
            return {"user_received_alert": None, "user_receiving_data": True}
        elif tracker.get_intent_of_latest_message() == 'user_deny':
            dispatcher.utter_template('utter_swap_transmitter', tracker)
            return {"user_receiving_data": None}
        else:
            dispatcher.utter_template('utter_doesnt_answer', tracker)
            return {}

    # Validation for the FID (must be a key in the FID dictionary)
    def validate_failure_id(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        if f'Failure ID {slot_value}' in fid_db:
            return {"failure_id": slot_value}
        else:
            dispatcher.utter_message(text='Invalid Failure ID')
            return {"failure_id": None}


# Action for showing the user the Failure Description -----------------------------------------------------------------
class ShowFailure(Action):

    def name(self) -> Text:
        return "action_show_failure"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the fid
        fid = tracker.get_slot("failure_id")
        failure = fid_db[f'Failure ID {fid}']
        # Tell user the failure
        dispatcher.utter_message(text=failure)

        return [AllSlotsReset()]


# Action for running weatherAPI ----------------------------------------------------------------------------------
class WeatherAPIClass(Action):

    activation_intent = 'ask_weather'  # user intent that activates this form

    def name(self) -> Text:
        return "weather_API"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            city_entity = tracker.latest_message['entities'][0]['value']
        except IndexError:
            dispatcher.utter_message(text="Sorry, I couldn't determine the city you're asking for")
            return []
        weather = get_weather(city_entity)
        dispatcher.utter_message(text=weather)
        return []


# Test Action for debugging purposes ----------------------------------------------------------------------------------
class TestAction(Action):
    def name(self) -> Text:
        return "action_test"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

        print("This is a test Action")

        return []


# Action for telling user about sensors -----------------------------------------------------------
class SensorChatter(Action):
    def name(self) -> Text:
        return "action_sensor_chatter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the sensor in question
        sensor_entity = tracker.latest_message['entities'][0]['value']
        #print (sensor_entity)

        # Get the description from the database
        sensor_desc = sensor_db[sensor_entity]
        #print(sensor_desc)

        # Tell the user the description
        dispatcher.utter_message(text=sensor_desc)
    