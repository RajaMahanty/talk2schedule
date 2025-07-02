import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

load_dotenv()

# Path to your service account JSON
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), "service_account.json")
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Load credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Build service
calendar_service = build("calendar", "v3", credentials=credentials)

# Use your primary calendar
CALENDAR_ID = 'djdevtest404@gmail.com'


def check_availability():
    ist = ZoneInfo("Asia/Kolkata")
    now = datetime.now(ist).replace(microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59)

    # Get today's events
    events_result = calendar_service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now.isoformat(),
        timeMax=end_of_day.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    # Parse event times
    busy_slots = []
    for event in events:
        start_str = event['start'].get('dateTime', event['start'].get('date'))
        end_str = event['end'].get('dateTime', event['end'].get('date'))

        start = datetime.fromisoformat(start_str).astimezone(ist)
        end = datetime.fromisoformat(end_str).astimezone(ist)
        busy_slots.append((start, end))

    # Sort just in case
    busy_slots.sort()

    # Find free slots between events
    free_slots = []
    pointer = now

    for start, end in busy_slots:
        if pointer < start:
            free_slots.append((pointer, start))
        pointer = max(pointer, end)

    if pointer < end_of_day:
        free_slots.append((pointer, end_of_day))

    if not free_slots:
        return "You're fully booked for the rest of today."

    # Format free slots
    slot_strings = []
    for start, end in free_slots:
        slot_strings.append(f"{start.strftime('%I:%M %p')} to {end.strftime('%I:%M %p')}")

    return "You're free during the following time slots today:\n" + "\n".join(slot_strings)


def book_appointment(start_time: datetime, end_time: datetime) -> str:
    event = {
        'summary': 'TailorTalk Appointment',
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }

    calendar_service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return f"📅 Appointment booked from {start_time.strftime('%I:%M %p')} to {end_time.strftime('%I:%M %p')} on {start_time.strftime('%b %d')} IST."

def book_appointment_default():
    ist = ZoneInfo("Asia/Kolkata")
    start_time = datetime.now(ist) + timedelta(hours=1)
    end_time = start_time + timedelta(minutes=30)
    return book_appointment(start_time, end_time)
