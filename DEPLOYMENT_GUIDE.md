# SEO Content Generator - Complete Guide

## Quick Start (Local)

### Prerequisites
- Python 3.10+
- Google Service Account credentials
- API Keys: OpenRouter, Gemini, Groq, OpenAI
- Supabase account
- Git

### 1. Setup Locally

```bash
# Clone or navigate to project
cd e:\aravindh\project

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file in project root:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-key
GOOGLE_SHEET_ID=your-sheet-id
GOOGLE_CREDENTIALS_FILE=secrets/google-service-account.json
GEMINI_API_KEY=your-key
GROQ_API_KEY=your-key
OPENAI_API_KEY=your-key
OPENROUTER_API_KEY=your-key
SCHEDULER_INTERVAL_SECONDS=20
```

### 3. Setup Google Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create service account
3. Download JSON key file
4. Save to `secrets/google-service-account.json`

### 4. Create Supabase Tables

1. Go to [Supabase](https://supabase.com)
2. Create new project
3. Run SQL from `supabase_schema.sql` in SQL editor

### 5. Run the App

```bash
python app/main.py
```

You'll see:
```
🚀 Admin panel available at http://localhost:8000/admin
📊 API available at http://localhost:8000/api/config
INFO: Uvicorn running on http://0.0.0.0:8000
```

### 6. Access Admin Panel

Open browser: `http://localhost:8000/admin`

You can now:
- Update Google Sheet ID
- Update all API keys
- Change scheduler interval
- Settings save immediately to `config.json`

---

## How to Use

### Add Content to Google Sheet

1. Open your Google Sheet
2. Add rows with format:

| Column A | Column B | Column C | Column E |
|----------|----------|----------|----------|
| Hospital Name | Service Type | Optional Details | Status |
| Example: "Medicare Hospital" | Example: "Emergency Care" | "24/7 Services" | `Pending` |

**Required:**
- ✅ Column A (Primary Input): Must have data
- ✅ Column B (Secondary Input): Must have data  
- ✅ Column C (Optional): Can be empty
- ✅ Column E (Status): Write `Pending`

**What happens:**
1. Scheduler checks every 20 seconds (or your configured interval)
2. App waits 3 seconds for optional input
3. Generates SEO content using OpenRouter (with fallbacks to Gemini, Groq)
4. Updates Column D with generated content
5. Updates Column E to `Completed` or `Failed`

### Update Configuration

1. Visit `http://localhost:8000/admin`
2. Update any fields (API keys, Sheet ID, etc.)
3. Click "Save Configuration"
4. Changes take effect immediately!

---

## Deployment Guide

### Option 1: Deploy to Render (Recommended - Easiest)

#### Step 1: Prepare Your Repository

```bash
git init
git add .
git commit -m "Initial commit"
git push origin main  # Push to GitHub
```

#### Step 2: Create on Render

1. Go to [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Fill in:
   - **Name:** `seo-content-generator`
   - **Region:** Select closest region
   - **Branch:** `main`
   - **Runtime:** `Python 3.10`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app/main.py`

#### Step 3: Add Environment Variables

In Render dashboard, go to Environment:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-key
GOOGLE_SHEET_ID=your-sheet-id
GOOGLE_CREDENTIALS_FILE=secrets/google-service-account.json
GEMINI_API_KEY=your-key
GROQ_API_KEY=your-key
OPENAI_API_KEY=your-key
OPENROUTER_API_KEY=your-key
SCHEDULER_INTERVAL_SECONDS=20
```

#### Step 4: Add Google Credentials

Create `secrets/google-service-account.json` in your repo with your service account JSON

#### Step 5: Deploy

Click "Deploy" and wait ~2-3 minutes

Your app will be live at: `https://your-service-name.onrender.com`

Access admin panel: `https://your-service-name.onrender.com/admin`

---

### Option 2: Deploy to Vercel

#### Step 1: Create Next.js Wrapper

Vercel prefers Node.js. Create `api/index.js`:
```javascript
import { spawn } from 'child_process';

export default async (req, res) => {
  // This won't work directly - use custom server instead
};
```

**Better: Use Render instead** (simpler for Python + long-running scheduler)

---

### Option 3: Deploy to Railway

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Connect repo
4. Add environment variables (same as Render)
5. Railway detects Python and auto-configures
6. Deploy!

---

## Troubleshooting

### Admin Panel Not Loading
- Check firewall allows port 8000
- Ensure FastAPI is installed: `pip install fastapi uvicorn`
- Check logs for errors

### Content Not Generating
- Check Google Sheet has correct columns
- Verify "Pending" status in Column E
- Check logs: `logs/app.log`
- Visit admin panel to verify API keys are correct

### Deployment Issues

**Render:**
- Check "Logs" tab in Render dashboard
- Ensure `python app/main.py` runs without errors locally first

**Railway:**
- Check build logs for pip install errors
- Ensure `.env` variables are set in Railway dashboard

---

## File Structure

```
project/
├── app/
│   ├── api/
│   │   └── admin.py          # Admin panel & API endpoints
│   ├── config/
│   │   ├── settings.py        # Settings from .env & config.json
│   │   └── config_manager.py  # JSON config persistence
│   ├── database/
│   │   └── client.py          # Supabase client
│   ├── repositories/          # Database operations
│   ├── services/
│   │   ├── seo_service.py     # Main orchestration
│   │   ├── google_sheet_service.py
│   │   ├── openrouter_service.py
│   │   ├── gemini_service.py
│   │   ├── groq_service.py
│   │   ├── openai_service.py
│   │   └── ai_router.py       # Provider failover
│   ├── scheduler/
│   │   └── scheduler.py       # APScheduler setup
│   ├── utils/
│   │   └── logger.py
│   └── main.py                # Entry point
├── secrets/
│   └── google-service-account.json  # Google credentials
├── logs/
│   └── app.log
├── config.json                # Runtime configuration (auto-created)
├── .env                       # Environment variables
├── requirements.txt
└── supabase_schema.sql
```

---

## Key Endpoints

### Admin Panel
- **GET** `http://localhost:8000/admin` - Admin UI

### API
- **GET** `/api/config` - Get current configuration
- **POST** `/api/config` - Update configuration

### Health Check
- **GET** `/docs` - FastAPI Swagger docs

---

## Important Notes

### For Production Deployment:

1. **config.json is NOT in git** (add to .gitignore)
   - This is where runtime settings are stored
   - Each deployment gets fresh `config.json`
   - Use admin panel to set values

2. **Environment variables (`.env`)** are for:
   - Supabase credentials (required)
   - Google Service Account path
   - Initial API keys (overridden by config.json)

3. **Scheduler runs 24/7**
   - No need for cron jobs
   - Long-running process on server
   - Handles graceful shutdown

4. **Concurrent Execution**
   - Scheduler runs in background task
   - FastAPI server handles requests
   - Both run simultaneously

---

## Monitoring

### Local
- Check `logs/app.log` for all activity
- Admin panel at `http://localhost:8000/admin`
- Check Google Sheet for updates

### Production (Render/Railway)
- View logs in dashboard
- Admin panel at `yourapp.com/admin`
- Check Google Sheet for updates

---

## Common Tasks

### Change API Key
1. Visit admin panel
2. Update "OpenRouter API Key"
3. Click Save
4. Done! Next request uses new key

### Change Google Sheet
1. Visit admin panel
2. Update "Google Sheet ID"
3. Click Save
4. Add new rows with "Pending" status

### Change Scheduler Interval
1. Visit admin panel
2. Update "Scheduler Interval (seconds)"
3. Click Save
4. Takes effect on next cycle

### View Processing Logs
```bash
tail -f logs/app.log  # Mac/Linux
Get-Content -Wait logs/app.log  # Windows PowerShell
```

---

## Summary

**Local Development:**
```bash
pip install -r requirements.txt
python app/main.py
# Visit http://localhost:8000/admin
```

**Production (Render):**
1. Push to GitHub
2. Create new Web Service on Render
3. Add environment variables
4. Deploy
5. Access at `https://yourapp.onrender.com/admin`

**That's it!** 🚀
