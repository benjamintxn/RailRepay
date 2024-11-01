import requests
from datetime import datetime

# A mapping of station names to CRS codes for a few SWR stations
station_codes = {
    'London Waterloo': 'WAT',
    'Clapham Junction': 'CLJ',
    'Woking': 'WOK',
    'Basingstoke': 'BSK',
    'Southampton Central': 'SOU',
    'Portsmouth Harbour': 'PMH',
    'Guildford': 'GLD',
    'Winchester': 'WIN',
    'Salisbury': 'SAL',
    'Reading': 'RDG',
    # Add more stations as needed
}

def get_station_code(station_name):
    return station_codes.get(station_name.title())

def main():
    print("Welcome to the SWR Delay Checker")
    date_input = input("Enter the date of travel (YYYY-MM-DD): ")
    time_input = input("Enter the scheduled departure time (HH:MM in 24-hour format): ")
    origin_input = input("Enter the origin station: ")
    destination_input = input("Enter the destination station: ")

    # Convert station names to CRS codes
    origin_code = get_station_code(origin_input)
    destination_code = get_station_code(destination_input)

    if not origin_code or not destination_code:
        print("Invalid station name(s). Please try again.")
        return

    # Build the API request
    app_id = 'd965e032'   # Replace with your TransportAPI app_id
    app_key = '1a50b50bb42e098d049e5cf9d5843938' # Replace with your TransportAPI app_key

    date = date_input
    time = time_input

    api_url = f"https://transportapi.com/v3/uk/train/station/{origin_code}/{date}/{time}/timetable.json"

    params = {
        'app_id': app_id,
        'app_key': app_key,
        'darwin': 'true',
        'train_status': 'passenger'
    }

    response = requests.get(api_url, params=params)

    if response.status_code != 200:
        print("Error fetching data from API.")
        return

    data = response.json()

    # Find the train the user is interested in
    found = False
    departures = data.get('departures', {}).get('all', [])
    if not departures:
        print("No departures found for the given time and station.")
        return

    fmt = '%H:%M'
    user_time = datetime.strptime(time_input, fmt)

    for departure in departures:
        # Debug: print departure information
        # print(departure)

        # Get the scheduled departure time of this train
        scheduled_departure = departure.get('aimed_departure_time')
        departure_time = datetime.strptime(scheduled_departure, fmt)

        # Check if the scheduled departure time matches the user's input time
        if departure_time == user_time:
            # Check if the destination CRS code matches
            destinations = departure.get('destination', [])
            destination_codes = [dest.get('crs') for dest in destinations]

            if destination_code in destination_codes:
                expected_departure = departure.get('expected_departure_time') or scheduled_departure
                expected_arrival = departure.get('expected_arrival_time') or departure.get('aimed_arrival_time')

                try:
                    expected_dep_time = datetime.strptime(expected_departure, fmt)
                except (TypeError, ValueError):
                    print("Expected departure time is not available.")
                    expected_dep_time = departure_time  # Assume on time

                dep_delay = (expected_dep_time - departure_time).total_seconds() / 60

                if dep_delay > 0:
                    print(f"The train was delayed by {dep_delay} minutes at departure.")
                else:
                    print("The train departed on time.")

                try:
                    scheduled_arrival = departure.get('aimed_arrival_time')
                    scheduled_arrival_time = datetime.strptime(scheduled_arrival, fmt)
                    expected_arrival_time = datetime.strptime(expected_arrival, fmt)
                except (TypeError, ValueError):
                    print("Arrival times are not available for this train.")
                    expected_arrival_time = scheduled_arrival_time = None

                if scheduled_arrival_time and expected_arrival_time:
                    arr_delay = (expected_arrival_time - scheduled_arrival_time).total_seconds() / 60

                    if arr_delay > 0:
                        print(f"The train was delayed by {arr_delay} minutes at arrival.")
                    else:
                        print("The train arrived on time.")
                else:
                    print("Arrival times are not available for this train.")

                found = True
                break  # Exit the loop after finding the train

    if not found:
        print("Could not find the train. Please check your inputs.")

if __name__ == '__main__':
    main()