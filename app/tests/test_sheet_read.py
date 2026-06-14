import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE')
SHEET_ID = os.getenv('GOOGLE_SHEET_ID')

if not CREDENTIALS_FILE or not SHEET_ID:
    print('ERROR: GOOGLE_CREDENTIALS_FILE or GOOGLE_SHEET_ID not set in .env')
    raise SystemExit(1)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

try:
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    range_name = 'A1:E10'
    result = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=range_name).execute()
    rows = result.get('values', [])
    print(f'Read {len(rows)} rows from sheet {SHEET_ID} (range {range_name}):')
    for r in rows[:10]:
        print(r)
except Exception as exc:
    print('Failed to read sheet:', exc)
    raise
