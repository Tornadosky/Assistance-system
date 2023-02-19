import requests
import datetime
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetMinMaxPrice(Action):

    def name(self) -> Text:
        return "action_get_minmax_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get value from time slot
        my_time = tracker.get_slot("time")
        print("time - ", my_time)
        # get value from person_type (Student, Employee, Others)
        person_type = tracker.get_slot("person_type")
        print("person type - ", person_type)

        print("detail = ", next(tracker.get_latest_entity_values("detail"), None))
        print("tracker = ", next(tracker.get_latest_entity_values("time"), None))
        print("all info - ", tracker.latest_message)

        detail = tracker.get_slot("detail")
        print("detail = ", detail)

        # default route - today
        if my_time is None:
            date = datetime.date.today()
        else:
            date = my_time[0:10]
            # specific time period (week)
            for obj in tracker.latest_message['entities']:
                # check for type of request (if it is a week)
                if obj['entity'] == "time" and obj['additional_info']['values'][0]['grain'] == "week":
                    
                    min_val, max_val = 100, -10
                    dish_name_min, dish_name_max = "", ""
                    date_plus = date

                    for i in range(5):
                        date_plus = (datetime.strptime(date_plus, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

                        x = requests.get(f'https://openmensa.org/api/v2/canteens/198/days/{date_plus}/meals')

                    
                    
                    response = "Sorry, seems like Mensa doesn't work this specific week."
                        
                    if detail == "cheap" and min_val < 50:
                        response = f"The cheapest dish for the week({date}) is '{dish_name_min}' with price {min_val} Euro"
                    if detail == "expensive" and max_val > 0:
                        response = f"The most expensive dish for the week({date}) is '{dish_name_max}' with price {max_val} Euro"
                    dispatcher.utter_message(response)
                    return []

        x = requests.get(f'https://openmensa.org/api/v2/canteens/198/days/{date}/meals')

        if (x.status_code == 404):
            response = "Sorry, we ran into problem with OpenMensa."
            dispatcher.utter_message(response) # send the message back to the user
            return []
        
        y = x.json()

        # calculate min price for specific day
        min_price, max_price = 100, -10
        for obj in y:
            if min_price > obj['prices'][person_type]:
                min_price = obj['prices'][person_type]
                dish_name_min = obj['name']
            if max_price < obj['prices'][person_type]:
                max_price = obj['prices'][person_type]
                dish_name_max = obj['name']
        
        response = "Sorry, seems like we have problem connecting to Mensa."

        dispatcher.utter_message(response)
        return []

class ActionGetPrice(Action):

    def name(self) -> Text:
        return "action_get_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get entity for specific dish
        dish = tracker.get_slot("dish")
        person_type = tracker.get_slot("person_type")
        
        # get value from time slot
        my_time = tracker.get_slot("time")

        # default route - today
        if my_time is None:
            date = datetime.date.today()
        else:
            date = my_time[0:10]

        x = requests.get(f'https://openmensa.org/api/v2/canteens/198/days/{date}/meals')

        if (x.status_code == 404):
            response = "Sorry, we ran into problem with OpenMensa."
            dispatcher.utter_message(response) # send the message back to the user
            return []
        
        y = x.json()
        # check in results if user's dish is at least partially in API results
        for obj in y:
            for part in dish.lower().split():
                if part in obj['name'].lower().split():
                    response = f"Price for { obj['name'] } is { obj['prices'][person_type] }"
                    dispatcher.utter_message(response)
                    return []

        response = f"Sorry, I couldn't find this dish in the menu for {date}."
        dispatcher.utter_message(response)
        return []

class ActionGetNotes(Action):

    def name(self) -> Text:
        return "action_get_notes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get entity for specific dish
        dish = tracker.get_slot("dish")
        my_time = tracker.get_slot("time")

        if dish is None:
            response = "Sorry, I couldn't understand what dish you want."
            dispatcher.utter_message(response)
            return []

        # default route - today
        if my_time is None:
            date = datetime.date.today()
        else:
            date = my_time[0:10]

        x = requests.get(f'https://openmensa.org/api/v2/canteens/198/days/{date}/meals')

        if (x.status_code == 404):
            response = "Sorry, we ran into problem with OpenMensa."
            dispatcher.utter_message(response)
            return []
        
        y = x.json()
        # check in results if user's dish is at least partially in API results
        for obj in y:
            for part in dish.lower().split():
                if part in obj['name'].lower().split():
                    response = f"Notes for { obj['name'] } are { obj['notes'] }"
                    dispatcher.utter_message(response)
                    return []

        response = "Sorry, I couldn't find this dish in the menu."
        dispatcher.utter_message(response)
        return []