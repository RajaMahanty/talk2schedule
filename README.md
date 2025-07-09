# TailorTalk

Book appointments with ease via chat! This project consists of a FastAPI backend (with Google Calendar and Gemini integration) and a Streamlit frontend.

---

## Project Structure

```
tailor_talk/
  backend/    # FastAPI backend (AI, calendar integration)
  frontend/   # Streamlit frontend (chat UI)
```

---

## 1. Backend Setup (FastAPI)

### Prerequisites

- Python 3.10+
- Google Cloud service account with Calendar API access

### Environment Variables

Create a `.env` file in `backend/` with:

```
GOOGLE_API_KEY=your_gemini_api_key_here
GOOGLE_CREDENTIALS_JSON='{"type": ... }'  # Entire service account JSON as a single line
```

- `GOOGLE_API_KEY`: Gemini API key (get from Google AI Studio)
- `GOOGLE_CREDENTIALS_JSON`: Paste the full service account JSON (as a string, escape quotes if needed)

### Install Dependencies

```
cd backend
pip install -r requirements.txt
```

### Run the Backend

```
uvicorn main:app --host 0.0.0.0 --port 8000
```

Or use the Procfile command for deployment:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 2. Frontend Setup (Streamlit)

### Prerequisites

- Python 3.10+

### Install Dependencies

```
cd frontend
pip install -r requirements.txt
```

### Run the Frontend

```
streamlit run app.py
```

Or use the Procfile command for deployment:

```
web: pip install -r requirements.txt && streamlit run app.py --server.port 8080 --server.enableCORS false
```

### Configure Backend URL

- By default, the frontend uses a deployed backend URL.
- For local development, edit `frontend/app.py` and set:
  ```python
  BACKEND_URL = "http://localhost:8000"
  ```

---

## 3. Google Calendar Setup

- Create a Google Cloud project and enable the Calendar API.
- Create a service account and download the JSON key.
- Paste the JSON (as a string) into your `.env` as `GOOGLE_CREDENTIALS_JSON`.
- Share your Google Calendar with the service account email.

---

## 4. Usage

- Start the backend and frontend as described above.
- Open the Streamlit app in your browser (default: http://localhost:8501).
- Chat to book appointments!

---

## 5. Deployment

- Use the provided `Procfile` in each directory for deployment to platforms like Heroku or Railway.
- Set environment variables in your deployment dashboard.

---

## 6. Troubleshooting

- Ensure all environment variables are set correctly.
- Check Google Cloud permissions and calendar sharing.
- For local development, make sure both backend and frontend are running and URLs match.

---

## License

MIT
