# ---------------------------------------------------------------
# PROJECT: SIMPLE AIRLINE BOOKING SYSTEM (FINAL SUBMISSION)
# PURPOSE: To simulate a real-world airline ticket booking process 
#          using Python concepts such as lists, functions, file handling, 
#          JSON data storage, and PDF generation. 
#          Includes a combined Admin Dashboard using Pandas & NumPy.
# ---------------------------------------------------------------
import json
import random
import time
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pandas as pd
import numpy as np

# ---- Step 1: Define flight data ----
flights = [
    {"flight_no": "AI101", "from": "Delhi", "to": "Mumbai", "price": 5500, "date": "2025-11-05 08:30"},
    {"flight_no": "AI202", "from": "Delhi", "to": "Chennai", "price": 7200, "date": "2025-11-05 12:00"},
    {"flight_no": "AI303", "from": "Bangalore", "to": "Kolkata", "price": 6400, "date": "2025-11-06 09:15"},
    {"flight_no": "AI404", "from": "Pune", "to": "Delhi", "price": 5800, "date": "2025-11-07 14:45"},
    {"flight_no": "AI505", "from": "Kolkata", "to": "Mumbai", "price": 8700, "date": "2025-11-08 10:30"}
]

BOOKING_FILE = "bookings.txt"


# ---- Step 2: Load and Save functions ----
def load_bookings():
    """Load all bookings from the text file safely."""
    try:
        with open(BOOKING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_bookings(bookings):
    """Save all bookings into the text file."""
    with open(BOOKING_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, indent=4)


# ---- Step 3: Display functions ----
def print_banner():
    print("\n" + "=" * 70)
    print(" SKYFLY AIRLINES – SIMPLE BOOKING SYSTEM ".center(70, "="))
    print("=" * 70)


def section_title(title):
    print("\n" + "-" * 70)
    print(title.center(70))
    print("-" * 70)


def show_flights():
    section_title("AVAILABLE FLIGHTS")
    print(f"{'Flight No.':<12}{'From':<15}{'To':<15}{'Departure':<22}{'Price (₹)':<10}")
    print("-" * 70)
    for f in flights:
        print(f"{f['flight_no']:<12}{f['from']:<15}{f['to']:<15}{f['date']:<22}{f['price']:<10}")
    print("-" * 70)


def search_flights():
    section_title("SEARCH FLIGHTS BY CITY")
    city = input("Enter the city name: ").strip().lower()
    found = False
    print()
    for f in flights:
        if city == f["from"].lower() or city == f["to"].lower():
            print(f"  {f['flight_no']} | {f['from']} → {f['to']} | {f['date']} | ₹{f['price']}")
            found = True
    if not found:
        print(f"No flights found related to {city.title()}.")
    print("-" * 70)


# ---- Step 4: Booking and Ticket ----
def book_ticket(bookings):
    section_title("BOOK A TICKET")
    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    show_flights()
    flight_no = input("Enter flight number to book: ").strip().upper()

    for flight in flights:
        if flight["flight_no"] == flight_no:
            print("\nProcessing your booking", end="")
            for _ in range(3):
                time.sleep(0.4)
                print(".", end="")
            print()

            booking_id = "SKY" + str(random.randint(1000, 9999))
            seat = f"{random.randint(1, 30)}{random.choice(['A','B','C','D','E','F'])}"

            booking = {
                "booking_id": booking_id,
                "name": name,
                "flight_no": flight["flight_no"],
                "from": flight["from"],
                "to": flight["to"],
                "price": flight["price"],
                "date": flight["date"],
                "seat": seat,
                "booking_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            bookings.append(booking)
            save_bookings(bookings)
            print("\nBooking Successful!")
            print_ticket(booking)
            create_fare_receipt_pdf(booking)
            return

    print("\nInvalid flight number.")


def print_ticket(booking):
    section_title("E-TICKET")
    print(f"Booking ID     : {booking['booking_id']}")
    print(f"Passenger Name : {booking['name']}")
    print(f"Flight Number  : {booking['flight_no']}")
    print(f"Route          : {booking['from']} → {booking['to']}")
    print(f"Departure      : {booking['date']}")
    print(f"Seat Number    : {booking['seat']}")
    print(f"Fare Amount    : ₹{booking['price']}")
    print(f"Booking Time   : {booking['booking_time']}")
    print("-" * 70)


def create_fare_receipt_pdf(booking):
    folder_path = os.path.join(os.path.expanduser("~"), "Documents", "Flight_Receipts")
    os.makedirs(folder_path, exist_ok=True)

    file_name = f"{booking['booking_id']}_Fare_Receipt.pdf"
    file_path = os.path.join(folder_path, file_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 60, "SKYFLY AIRLINES")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Fare Receipt for {booking['name']}")
    c.line(50, height - 105, width - 50, height - 105)

    y = height - 140
    details = [
        f"Booking ID     : {booking['booking_id']}",
        f"Passenger Name : {booking['name']}",
        f"Flight Number  : {booking['flight_no']}",
        f"Route          : {booking['from']} → {booking['to']}",
        f"Departure Time : {booking['date']}",
        f"Seat Number    : {booking['seat']}",
        f"Fare Amount    : ₹{booking['price']}",
        f"Booking Time   : {booking['booking_time']}",
        "",
        "Status         : Confirmed"
    ]
    for d in details:
        c.drawString(70, y, d)
        y -= 20

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(70, y - 10, "Thank you for flying with SkyFly Airlines!")
    c.save()

    print(f"\nFare Receipt saved to: {file_path}")


# ---- Step 5: View, Cancel, Admin Dashboard ----
def view_bookings(bookings):
    section_title("MY BOOKINGS")
    if not bookings:
        print("No bookings found.")
        print("-" * 70)
        return
    print(f"{'Booking ID':<12}{'Name':<15}{'Flight':<10}{'Route':<22}{'Seat':<8}{'Fare(₹)':<10}")
    print("-" * 70)
    for b in bookings:
        route = f"{b['from']}→{b['to']}"
        booking_id = b.get('booking_id', 'N/A')
        print(f"{booking_id:<12}{b['name']:<15}{b['flight_no']:<10}{route:<22}{b['seat']:<8}{b['price']:<10}")
    print("-" * 70)


def cancel_booking(bookings):
    section_title("CANCEL BOOKING")
    name = input("Enter your name: ").strip()
    flight_no = input("Enter flight number to cancel: ").strip().upper()

    for b in bookings:
        if b["name"].lower() == name.lower() and b["flight_no"] == flight_no:
            confirm = input(f"Confirm cancellation for booking {b.get('booking_id', 'N/A')}? (y/n): ").lower()
            if confirm == 'y':
                bookings.remove(b)
                save_bookings(bookings)
                print("\nBooking cancelled successfully.")
                return
            else:
                print("Cancellation aborted.")
                return
    print("\nNo such booking found.")


def admin_dashboard():
    """Combined Admin Summary + Data Analytics using Pandas & NumPy."""
    section_title("ADMIN DASHBOARD (SUMMARY + ANALYTICS)")
    password = input("Enter admin password: ")
    if password != "admin123":
        print("Wrong password.")
        return

    bookings = load_bookings()
    if not bookings:
        print("No bookings available for analysis.")
        return

    df = pd.DataFrame(bookings)
    prices = np.array(df["price"])

    print("\n--- OVERALL SUMMARY ---")
    print(f"Total Bookings       : {len(df)}")
    print(f"Total Revenue        : ₹{np.sum(prices)}")
    print(f"Average Fare         : ₹{np.mean(prices):.2f}")
    print(f"Highest Fare         : ₹{np.max(prices)}")
    print(f"Lowest Fare          : ₹{np.min(prices)}")

    top_route = df.groupby(["from", "to"]).size().idxmax()
    print(f"Most Popular Route   : {top_route[0]} → {top_route[1]}")

    print("\n--- REVENUE BY CITY ---")
    for city, value in df.groupby("from")["price"].sum().items():
        print(f"  {city:<12} ₹{value}")

    print("\n--- SAMPLE BOOKINGS ---")
    print(df[["booking_id", "name", "flight_no", "from", "to", "price"]].head())

    print("\nDashboard analysis completed successfully.")
    print("-" * 70)


# ---- Step 6: Main Menu ----
def main_menu():
    bookings = load_bookings()
    while True:
        print_banner()
        print("1. View Available Flights")
        print("2. Search Flights by City")
        print("3. Book a Ticket")
        print("4. View My Bookings")
        print("5. Cancel a Booking")
        print("6. Admin Dashboard (Summary + Analytics)")
        print("7. Exit")
        print("=" * 70)
        choice = input("Enter your choice (1–7): ").strip()

        if choice == '1':
            show_flights()
        elif choice == '2':
            search_flights()
        elif choice == '3':
            book_ticket(bookings)
        elif choice == '4':
            view_bookings(bookings)
        elif choice == '5':
            cancel_booking(bookings)
        elif choice == '6':
            admin_dashboard()
        elif choice == '7':
            print("\nThank you for choosing SkyFly Airlines. Have a safe journey!")
            print("=" * 70)
            break
        else:
            print("\nInvalid input. Please choose between 1–7.")

        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main_menu()
