# SEO Content Generator Automation System

A production-ready Python service that reads pending SEO keyword rows from Google Sheets, stores requests in Supabase, generates unique SEO copy with AI provider failover, writes content back to Google Sheets, and logs everything with fault-tolerant flow.

## Features

- Reads new rows from Google Sheets every 5 minutes
- Stores request metadata in Supabase
- Generates SEO copy using Gemini, Groq, then OpenAI failover
- Prevents content repetition within the last 7 days
- Stores generated content history
- Writes content back to Google Sheets
- Logs structured events and errors
- Uses RotatingFileHandler for production logging

## Project Structure

```
project/
│
├── app/
│   ├── api/
│   ├── config/
│   ├── database/
│   ├── scheduler/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── prompts/
│   ├── utils/
│   └── main.py
├── requirements.txt
├── .env.example
├── Dockerfile
└── docker-compose.yml
```

## Getting Started

1. Copy `.env.example` to `.env` and fill in credentials.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Run the service:

```bash
python app/main.py
```

## Docker

Build and run with Docker:

```bash
docker build -t seo-generator .
```

Run with docker-compose:

```bash
docker compose up -d
```

## Notes

- The system is designed to run automatically every 5 minutes.
- `Status` values in Google Sheets are `Pending`, `Processing`, `Completed`, and `Failed`.
- All generated content is persisted in Supabase for duplication checks.
- Failure logs are saved to `logs/app.log` and to the `system_logs` table.
