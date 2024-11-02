# traindelay.py
import sys
from services import ServiceMetric, ServiceDetail
from utils import arg_parse, calculate_delay, get_refund_percentage
from policies import TOC_REFUND_POLICIES, TOC_NAMES

if __name__ == "__main__":
    from_loc, to_loc, time_str, date_str = arg_parse(sys.argv[1:])  # Parse command-line arguments

    sm = ServiceMetric(from_loc, to_loc, date_str, time_str)
    sm.post_service_metrics()  # Send POST request to Service Metrics

    # Get RIDs for the service matching the scheduled departure time
    rids = []
    for service in sm.response.json().get("Services", []):
        gbtt_ptd = service["serviceAttributesMetrics"].get("gbtt_ptd", "")
        if gbtt_ptd == sm.from_time:
            rids.extend(service["serviceAttributesMetrics"].get("rids", []))

    if not rids:
        print("No service match.")
        sys.exit()

    sd = ServiceDetail(rids[0])
    sd.post_service_detail()  # Send POST request to Service Details

    toc_code = sd.toc_code
    # Check if the train is operated by one of the supported TOCs
    if toc_code not in TOC_REFUND_POLICIES:
        print("The railway provider is not compatible. Supported operators are:")
        for code, name in TOC_NAMES.items():
            print(f"- {name} ({code})")
        sys.exit()

    operator_name = TOC_NAMES.get(toc_code, 'Unknown Operator')

    # Proceed if it's a supported TOC
    train = sd.response.json()["serviceAttributesDetails"]["locations"]
    for station in train:
        if station["location"] == sm.to_loc:
            scheduled_arrival = station.get('gbtt_pta')
            actual_arrival = station.get('actual_ta')
            if not scheduled_arrival or not actual_arrival:
                print("Could not retrieve arrival times.")
                sys.exit()

            print(f"Journey: {from_loc.upper()} --> {to_loc.upper()}")
            print(f"Operator: {operator_name}")
            print(f"Scheduled Arrival: {scheduled_arrival}")
            print(f"Actual Arrival: {actual_arrival}")

            # Calculate delay
            delay_minutes = calculate_delay(scheduled_arrival, actual_arrival)
            print(f"Delay: {delay_minutes} minutes")

            # Determine refund percentage
            refund_percentage, ticket_type = get_refund_percentage(toc_code, delay_minutes)
            if refund_percentage > 0:
                print(f"You are eligible for a {int(refund_percentage * 100)}% refund on your {ticket_type} fare.")
                # Ask user for ticket price
                try:
                    ticket_price = float(input("Enter the amount you paid for the ticket in GBP: £"))
                except ValueError:
                    sys.exit("Invalid input for ticket price.")

                compensation = ticket_price * refund_percentage
                print(f"You can get compensated: £{compensation:.2f}")
            else:
                print("You are not eligible for a refund.")

            break
    else:
        print("Destination station not found in service details.")