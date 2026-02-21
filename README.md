# UNLISTED O’RENA - PRIVATE MARKET INTELLIGENCE TERMINAL

A comprehensive full-stack terminal application designed to generate professional, institutional-grade equity research reports for unlisted Indian companies. Powered by FastAPI, OpenAI's GPT-4o, and highly structured Pydantic models.

## Features
- **FastAPI Backend**: Asynchronous architecture providing high performance.
- **Strict Format Pydantic V2 Models**: Enforces a rigid 12-section institutional report format containing textual analysis, bulleted lists, and structured financial tables.
- **AI Analytics Engine**: Utilizes OpenAI GPT-4o to analyze targeted unlisted companies and return structured JSON. Focuses on INR Crores and strictly formats simulated financial tables, comparative ratios, unit economics, cap structure, and projections.
- **Professional Minimalist UI**: Clean, institutional frontend layout with collapsible research sections mimicking top-tier intelligence terminals. Built with vanilla HTML/CSS/JS (no framework bloat).
- **Direct Exports**: Generates native DOCX and highly-formatted PDF downloads on the fly (using `python-docx` and `xhtml2pdf`), preserving tables, disclaimers, and institutional headers/footers.

## Project Structure
```text
.
├── backend/
│   ├── main.py                 # FastAPI routing and entrypoint
│   ├── models.py               # Pydantic schemas enforcing the 12-section layout
│   ├── requirements.txt        # Python 3+ requirements
│   ├── .env.example            # Environment sample
│   └── services/
│       ├── ai_service.py       # Prompt engineering and OpenAI implementation
│       └── export_service.py   # PDF and DOCX file compilation logic
├── frontend/
│   ├── index.html              # Frontend UI / Terminal dashboard
│   ├── css/
│   │   └── styles.css          # Minimalist terminal styling
│   └── js/
│       └── app.js              # Render logic and PDF/DOCX routing
└── README.md
```

## Running the Terminal Locally

1. **Prerequisites**
   Ensure Python 3.10+ is installed on your system.
   
2. **Setup Virtual Environment**
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   # source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Environment Variables**
   Rename `backend/.env.example` to `backend/.env` and insert your API credentials:
   ```env
   OPENAI_API_KEY=sk-proj-your-api-key-here
   ```

5. **Start the Uvicorn Server**
   To ensure static files are mounted correctly, run the server from the project root!
   ```bash
   # Make sure you are in the root directory 'd:\PRECONET\Research report\'
   # DO NOT run from inside the backend/ directory!
   uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
   ```

6. **Access the Application**
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your modern web browser.

## Upgrade Guidance (Moving to Real Financial APIs)
The application architecture isolates the data generation inside `backend/services/ai_service.py`. 
To upgrade the terminal to use verified real-time financial data:
1. Connect to an external market API (e.g. Tracxn, Crunchbase API, etc.) inside `ai_service.py`.
2. Extract historical financials, ratios, and peer matrices programmatically.
3. Pass structured data directly into the `ResearchReport` Pydantic models.
4. Pass the qualitative sections to GPT-4o with the real financial data injected as context to generate accurate analysis summaries. 
5. The frontend and export logic (PDF/DOCX) requires **zero changes** as long as you maintain the `ResearchReport` structure.
