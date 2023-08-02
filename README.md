# Train Seat Reservation System

The Train Seat Reservation System is a Django-based backend API that allows families to reserve seats in the same cabin based on the number of members in the family. The system ensures that all family members are seated together to provide a comfortable travel experience.

## Features

- Seat Reservation: Users can initiate the seat reservation process for their family, select the number of family members, and reserve seats in the same cabin.
- Cabin Class Selection: Users can choose their preferred cabin class (e.g., first class, second class).
- Seat Availability Check: The system checks the availability of seats in the selected cabin and suggests alternatives if seats are not available.
- Seat Information: The system retrieves seat information, including seat numbers and fares for the selected cabin class.
- Reservation ID: The system generates a unique reservation ID for each booking and provides it to the user.
- Fare Calculation: The total fare for the reservation is calculated based on the selected seats.
- Booking Confirmation: Reserved seats are marked as occupied, and the user receives reservation details and payment links.

## Requirements

- Python 3.x
- Django 3.x
- Django REST framework 3.x

## Installation

1. Clone the repository:
3. Install the required packages: `pip install -r requirements.txt`
4. create database schema: `python manage.py makemigrations`
5. migrate database schema: `python manage.py migrate`
6. Run the development server: `python manage.py runserver`
7. Access the API at `http://localhost:8000/`

## API Endpoints

- `POST /createCabin`: Create a new cabin with a specific name and total seats capacity.
 Input Payload Example:
  ```json
  {
    "cabinName": "First Class",
    "totalSeats": 50
  }
- `PATCH /updateCabin`: Update the total seats capacity of an existing cabin.
  Input Payload Example:
  ```json
  {
    "cabinName": "First Class",
    "totalSeats": 100
  }
- `POST /addSeat`: Add a new seat to an existing cabin with the specified seat number and fare.
Payload:
  ```json
  {
      "cabinName": "First Class",
      "seatNumber": "A1",
      "fare": 100
  }
- `GET /getCabinInfo`: Get information about a specific cabin by its name.
 Input Query Parameter: `?cabinName=First%20Class`
- `POST /checkSeatAvailability`: Check seat availability in a cabin for a given number of seats.
   Payload
   ```json
  {
     "seatCount": 100,
     "cabinName": "First Class"
  }
- `POST /bookSeats`: Book seats for a family in a cabin based on the number of family members.
  Payload
  ```json
  {
     "seatNumbers": [A1],
     "cabinName": "First Class"
  }
## Testing

To run the tests for the API, use the following command: `python .\manage.py test api`


