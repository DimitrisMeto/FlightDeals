from data_manager import DataManager
from pprint import pprint
import datetime as dt
from flight_search import FlightSearch
from notification_manager import NotificationManager

notification_manager = NotificationManager()
flight_search = FlightSearch()

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()


if sheet_data[0]["iataCode"] == "":
    for location in sheet_data:
        location["iataCode"] = flight_search.get_destination_code(city_name=location["city"])

    pprint(sheet_data)
    data_manager.destination_data = sheet_data
    data_manager.update_destination_data()

ORIGIN_CITY = "LON"

now = dt.date.today()
tomorrow = now + dt.timedelta(days=1)
six_months = now + dt.timedelta(days=6*30)

for destination in sheet_data:
    flight = flight_search.check_flights(origin_city_code=ORIGIN_CITY, destination_city_code=destination["iataCode"],
                                         from_time=tomorrow, to_time=six_months)

    if flight is None:
        continue

    if flight.price < destination["lowestPrice"]:
        users = data_manager.get_users_emails()
        emails = [entry["email"] for entry in users]
        names = [entry["firstName"] for entry in users]

        message = f"Low price alert! Only £{flight.price} to fly from "  f"{flight.departure_city}-{flight.departure_airport}" \
             f" to "f"{flight.origin_city}-{flight.origin_airport} from {flight.out_date} "f"to {flight.return_date}."

        if flight.stop_overs > 0:
            message += F"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
            print(message)

        link = f"https://www.google.co.uk/flights?hl=en#flt={flight.departure_airport}.{flight.origin_airport}" \
               f".{flight.out_date}*{flight.origin_airport}.{flight.departure_airport}.{flight.return_date}"
        notification_manager.send_emails(message=message, emails=emails, google_flight_link=link)
