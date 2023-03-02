from flight_data import FlightData
import requests
import pprint
import os

SEARCH_FLIGHT_API = "http://api.tequila.kiwi.com"
SEARCH_FLIGHT_API_KEY = os.environ.get("API_KEY")


class FlightSearch:

    def get_destination_code(self, city_name):
        header = {
            "apikey": SEARCH_FLIGHT_API_KEY
        }

        params = {
            "term": city_name,
            "location_types": "city"
        }

        tequila_response = requests.get(url=f"{SEARCH_FLIGHT_API}/locations/query", params=params, headers=header)
        tequila_data = tequila_response.json()["locations"]
        code = tequila_data[0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time,
            "date_to": to_time,
            "nights_in_dst_from": "7",
            "nights_in_dst_to": "28",
            "flight_type": "round",
            "one_for_city": "1",
            "curr": "GBP",
            "max_stopovers": "0"
        }

        header = {
            "apikey": SEARCH_FLIGHT_API_KEY
        }

        response = requests.get(url=f"{SEARCH_FLIGHT_API}/v2/search", params=query, headers=header)

        try:
            data = response.json()["data"][0]
        except IndexError:
            try:
                query["max_stopovers"] = 1
                response = requests.get(url=f"{SEARCH_FLIGHT_API}/v2/search", params=query, headers=header)
                data = response.json()["data"][0]
                pprint.pprint(data)

                flight_data = FlightData(price=data["price"], departure_city=data["route"][0]["cityFrom"],
                                         departure_airport=data["route"][0]["flyFrom"],
                                         origin_city=data["route"][1]["cityTo"], origin_airport=data["route"][1]["flyTo"],
                                         out_date=data["route"][0]["local_departure"].split("T")[0],
                                         return_date=data["route"][2]["local_departure"].split("T")[0], stop_overs=1,
                                         via_city=data["route"][0]["cityTo"])
                return flight_data

            except IndexError:
                print(f"No flights found for {destination_city_code}.")
                return None

        else:
            flight_data = FlightData(price=data["price"], origin_city=data["cityTo"], departure_city=data["cityFrom"],
                                     origin_airport=data["flyTo"], departure_airport=data["flyFrom"],
                                     out_date=data["route"][0]["local_departure"].split("T")[0],
                                     return_date=data["route"][1]["local_departure"].split("T")[0])

            print(f"{flight_data.origin_city}: £{flight_data.price}")
            return flight_data
