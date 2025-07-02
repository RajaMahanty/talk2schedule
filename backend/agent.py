import os
import google.generativeai as genai
from dotenv import load_dotenv
from calendar_tools import check_availability, book_appointment
from session_memory import set_proposed_slot, get_proposed_slot, clear_proposed_slot
from dateutil.parser import parse as parse_datetime
from zoneinfo import ZoneInfo
import re

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY"),
    transport="rest"
)

model = genai.GenerativeModel("gemini-1.5-flash")

def run_agent(user_input: str) -> str:
    try:
        ist = ZoneInfo("Asia/Kolkata")
        lowered = user_input.lower()

        # ✅ Step 1: Confirm slot
        if any(word in lowered for word in ["yes", "book it", "confirm", "go ahead"]):
            slot = get_proposed_slot()
            if slot:
                start, end = slot
                clear_proposed_slot()
                result = book_appointment(start, end)                
                return model.generate_content(
                    f"The appointment has been booked. Reply to user: '{result}'"
                ).text
            else:
                return "I don't have a time slot ready to book. Could you please tell me your preferred time?"

        # ✅ Step 2: Ask Gemini if this is a booking intent
        tool_prompt = f"""
You are helping a user schedule appointments.

If the user provides a preferred time (e.g., "Book me for 3pm tomorrow"), extract the time as:
START: 2025-07-02T15:00:00+05:30
END: 2025-07-02T15:30:00+05:30

If no specific time is mentioned, respond with TOOL: check_availability or just respond naturally.

User: "{user_input}"
"""
        route = model.generate_content(tool_prompt).text.strip()

        # ✅ Step 3: Handle extracted booking
        if route.startswith("START:"):
            try:
                # Extract times using regex (safe even if extra text is added)
                start_match = re.search(r"START:\s*(.+)", route)
                end_match = re.search(r"END:\s*(.+)", route)

                if not (start_match and end_match):
                    raise ValueError("Could not find START/END in Gemini output.")

                start = parse_datetime(start_match.group(1)).astimezone(ist)
                end = parse_datetime(end_match.group(1)).astimezone(ist)

                # Save to memory
                set_proposed_slot(start, end)

                return model.generate_content(
                    f"""The user wants to book an appointment. Confirm with them if this slot is okay:
{start.strftime('%I:%M %p')} to {end.strftime('%I:%M %p')} IST on {start.strftime('%b %d')}"""
                ).text

            except Exception as e:
                return f"⚠️ Couldn’t understand the requested time. Please rephrase. Error: {e}"

        # ✅ Step 4: Availability
        elif "TOOL: check_availability" in route:
            raw = check_availability()
            return model.generate_content(
                f"""The user said: "{user_input}"
Here are the available free slots today: {raw}
Respond politely with useful info."""
            ).text

        # ✅ Step 5: Default Gemini chat
        return route

    except Exception as e:
        print("ERROR in run_agent:", e)
        return "⚠️ Something went wrong while processing your request."
