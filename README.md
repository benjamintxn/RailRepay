# RailRepay

RailRepay is a command-line application that interacts with the National Rail Darwin Data Feeds Historical Service Performance (HSP) APIs to help UK train passengers calculate potential compensation due to train delays. It determines the delay duration, checks eligibility based on various Train Operating Companies’ (TOCs) Delay Repay policies, and calculates the refund amount.

## Motivation

Train delays are a common inconvenience for passengers in the UK. While compensation schemes like Delay Repay exist, determining eligibility and calculating the refund amount can be confusing due to varying policies across different TOCs. RailRepay simplifies this process by providing an easy-to-use tool that calculates potential compensation based on actual train performance data.

## Roadmap

Future enhancements planned for RailRepay include:

- Support for Additional TOCs: Expand compatibility to include more train operators with their respective refund policies.
- Multi-Leg Journeys: Allow users to input journeys with multiple legs and calculate total delays and compensation.
- Automated Claim Submission: Integrate with TOCs’ online systems to automate the submission of compensation claims.
- Graphical User Interface (GUI): Develop a user-friendly GUI for easier interaction.
- Data Validation: Implement station code validation and more robust input handling.

## Installation

Ensure you have Python 3.7+ (https://www.python.org/downloads/) installed on your system.

### Clone the Repository

```bash
git clone https://github.com/benjamintxn/railrepay.git
cd railrepay
```

### Set Up a Virtual Environment (Optional but Recommended)

Create and activate a virtual environment to manage dependencies:

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Set Up Environment Variables

RailRepay requires access to the National Rail Darwin Data Feeds HSP API. You need to obtain credentials by registering on the National Rail Data Portal (https://opendata.nationalrail.co.uk).

Set the following environment variables with your credentials:

```bash
# On Windows:
set DARWIN_EMAIL=your_email@example.com
set DARWIN_PASS=your_password

# On macOS/Linux:
export DARWIN_EMAIL='your_email@example.com'
export DARWIN_PASS='your_password'
```

Alternatively, you can create a .env file in the project root:

```bash
DARWIN_EMAIL=your_email@example.com
DARWIN_PASS=your_password
```

## Usage

The general syntax is:

```bash
python traindelay.py <origin_station_code> <destination_station_code> <departure_time> <journey_date>
```

- <origin_station_code>: CRS code of the departure station (e.g., WAT for London Waterloo).
- <destination_station_code>: CRS code of the arrival station (e.g., WOK for Woking).
- <departure_time>: Scheduled departure time in HHMM 24-hour format (e.g., 0653 for 6:53 AM).
- <journey_date>: Date of the journey in YYYY-MM-DD format (e.g., 2023-10-14).

### Example: London Waterloo to Woking

```bash
python traindelay.py WAT WOK 0653 2023-10-14
```

### Sample Output:

```bash
Journey: WAT --> WOK
Operator: South Western Railway
Scheduled Arrival: 0726
Actual Arrival: 0745
Delay: 19 minutes
You are eligible for a 25% refund on your single fare.
Enter the amount you paid for the ticket in GBP: £20.00
You can get compensated: £5.00
```

### Supported Train Operators

- East Midlands Railway (EM)
- South Western Railway (SW)
- Great Western Railway (GW)
- Chiltern Railways (CH)
- CrossCountry (XC)
- Southeastern (SE)

## Project Structure

- traindelay.py: Main script to run the application.
- services.py: Contains classes for API interactions (ServiceMetric, ServiceDetail).
- utils.py: Utility functions for argument parsing and calculations.
- policies.py: Definitions of refund policies and operator names.
- constants.py: Constants used across the application.
- requirements.txt: List of Python package dependencies.

## Contact

For questions or suggestions, please open an issue on the GitHub repository (https://github.com/benjamintxn/RailRepay/issues).

## Licensing

- Parts of this project are based on code from the train-delay project by Alex Gregory, used under the MIT License.
- The original MIT License and copyright notice are included.

Disclaimer: This tool is intended to assist users in calculating potential compensation due to train delays. The actual compensation may vary based on the train operating company’s policies and the accuracy of the data provided by the National Rail APIs. Users should verify the information and consult the relevant train operator for official claims.