import requests
from pprint import pprint

USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
SHEET_API = "https://api.sheety.co/a3e2c33d40aaba95ce3030d04045f9ad/myFlightDeals/prices"
USERS_API = "https://api.sheety.co/a3e2c33d40aaba95ce3030d04045f9ad/myFlightDeals/users"

class DataManager:

    def __init__(self):
        self.destination_data = []
        self.user_data = []
    def get_destination_data(self):
        sheety_response = requests.get(url=SHEET_API, auth=(USERNAME, PASSWORD))
        data_sheety = sheety_response.json()
        # pprint(self.data_sheety)
        self.destination_data = data_sheety["prices"]
        return self.destination_data

    def update_destination_data(self):
        for location in self.destination_data:
            row_id = location["id"]

            parameters = {
                "price": {
                    "iataCode": location["iataCode"]
                }
            }

            update_response = requests.put(url=f"{SHEET_API}/{row_id}", json=parameters, auth=(USERNAME, PASSWORD))
            # print(update_response.text)

    def get_users_emails(self):
        response_users = requests.get(url=USERS_API, auth=(USERNAME, PASSWORD))
        data_users = response_users.json()
        self.user_data = data_users["users"]
        return self.user_data
