from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset

from action_utils import get_dict, get_last_bot_event


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
class weatherAPIClass(Action):

    activation_intent = 'ask_weather'  # user intent that activates this form


    def name(self) -> Text:
        return "weather_API"

    
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        slot_value: Any,
        domain: "DomainDict",
        ) -> List[Dict[Text, Any]]:
	

        if tracker.get_intent_of_latest_message() == self.activation_intent:

            # import required modules 
            import requests, json

            # Enter your API key here 
            api_key = "bd2f89be8d346be8d67f39c35098ac29"

            # base_url variable to store url
            base_url = "http://api.openweathermap.org/data/2.5/weather?"

            # Give city name 
            city_name = slot_value;

            # complete_url variable to store 
            # complete url address 
            complete_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city_name,api_key)

            # get method of requests module 
            # return response object 
            response = requests.get(complete_url)

            # json method of response object  
            # convert json format data into 
            # python format data 
            x = response.json()

            # Now x contains list of nested dictionaries 
            # Check the value of "cod" key is equal to 
            # "404", means city is found otherwise, 
            # city is not found 
            if x["cod"] != "404":

                # store the value of "main" 
                # key in variable y 
                y = x["main"]

                # store the value corresponding 
                # to the "temp" key of y 
                current_temperature = y["temp"]

                # store the value corresponding 
                # to the "pressure" key of y 
                current_pressure = y["pressure"]

                # store the value corresponding 
                # to the "humidity" key of y 
                current_humidiy = y["humidity"]

                # store the value of "weather" 
                # key in variable z 
                z = x["weather"]

                # store the value corresponding  
                # to the "description" key at  
                # the 0th index of z 
                weather_description = z[0]["description"]
                x=(" Temperature (in kelvin unit) = " +
                      str(current_temperature) +
                      "\n atmospheric pressure (in hPa unit) = " +
                      str(current_pressure) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

                # print following values 
                print(" Temperature (in kelvin unit) = " +
                      str(current_temperature) +
                      "\n atmospheric pressure (in hPa unit) = " +
                      str(current_pressure) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

            else:
                x=(" City Not Found ")
                print(" City Not Found ") 


        dispatcher.utter_message(text=x)
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

        print(fid_db)

        return []
