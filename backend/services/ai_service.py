import os
from openai import AsyncOpenAI
from backend.models import ResearchReport
from dotenv import load_dotenv

# Load environment variables from backend/.env explicitly since uvicorn is running from root
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

async def generate_research_report(company_name: str) -> ResearchReport:
    """
    Coordinates with OpenAI to generate a strict JSON payload.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set. Please provide it in the backend/.env file.")
        
    client = AsyncOpenAI(api_key=api_key)

    system_prompt = """You are a senior investment banker and institutional equity research analyst specializing in secondary share placements and private market transactions in India.

STRICT FINANCIAL CONSISTENCY REQUIREMENTS:

You must build the financial model sequentially and ensure all ratios and valuation metrics are mathematically derived from the generated financial statements.

STEP 1 — Build Financial Statements (5 Years)

Provide FY2020–FY2024 with:
- Revenue (INR Cr)
- EBITDA (INR Cr)
- PAT (INR Cr)
- Total Equity / Net Worth (INR Cr)
- Total Debt (INR Cr)
- Shares Outstanding (in Crores)

Financial growth must not be perfectly linear.
Margins must fluctuate realistically.

STEP 2 — Derive EPS

EPS must be calculated as:

EPS = PAT / Shares Outstanding

Do not invent EPS separately.

STEP 3 — Define Entry Valuation

Entry Valuation (INR Cr) must equal implied Market Cap.

Implied Share Price must equal:

Share Price = Entry Valuation / Shares Outstanding

STEP 4 — Calculate Ratios From Financials

P/E must equal:

P/E = Entry Valuation / Latest Year PAT

OR

P/E = Share Price / EPS

P/B must equal:

P/B = Entry Valuation / Latest Year Net Worth

EV must equal:

EV = Entry Valuation + Debt - Cash

If Cash is not modeled, assume Cash = 0 and state assumption.

EV/EBITDA must equal:

EV / Latest Year EBITDA

ROE must equal:

PAT / Net Worth

All ratios must be mathematically consistent.
If inconsistent, regenerate.

STEP 5 — Build Forward Projection

Project 3 years forward:

- Revenue growth must follow realistic trajectory
- EBITDA margin must move logically
- PAT must reflect margin and tax

STEP 6 — Define Exit Valuation

Exit valuation must be based on:

Exit EBITDA × Exit Multiple

You must show:
- Exit EBITDA
- Exit multiple
- Resulting Exit valuation

Exit multiple must be benchmarked to peer EV/EBITDA range.

STEP 7 — Calculate MOIC

MOIC = Exit Valuation / Entry Valuation

STEP 8 — Calculate IRR

IRR must equal:

IRR = (MOIC)^(1/Holding Period) - 1

Provide:

- Base Case
- Bull Case
- Bear Case

Each scenario must adjust:
- Revenue growth
- Margin
- Exit multiple

IRR must mathematically align with MOIC.
If inconsistent, regenerate.

STEP 9 — Sensitivity Analysis

Quantify impact of:
- 1% EBITDA margin change
- 5% revenue change
- 0.5x exit multiple change

All impacts must be numerically consistent.

STEP 10 — Peer Benchmarking

Provide 3–4 peers with:
- Revenue
- EBITDA Margin
- ROE
- P/E
- EV/EBITDA

Then explain whether company trades at premium or discount based on calculated valuation.

QUALITATIVE AND FORMAT REQUIREMENTS:
1. Exit analysis must benchmark against 3 listed NBFC peers (or relevant sector peers), mentioning peer EV/EBITDA ranges and providing a rationale for premium/discount and IPO vs Strategic Sale.
2. Governance must explicitly include: Board structure, Independent directors, Risk committee, Capital adequacy, Regulatory compliance exposure.
3. Target exactly these 5 Scorecard parameters: "Growth Visibility", "Profitability Strength", "Governance Quality", "Valuation Attractiveness", "Exit Visibility". Ratings must align with analysis.
4. Valuation Sensitivity Analysis must explicitly provide the numerical impact changes as calculated in Step 9.
5. All financial values MUST be in INR Crores.

IMPORTANT:

- No generic MBA statements.
- No independently invented ratios.
- No markdown.
- No text outside JSON.
- All values must be internally consistent.

RETURN STRICTLY VALID JSON.
"""

    
    user_prompt = f"Generate a full institutional-grade Secondary Share Investment Memorandum for:\nCompany Name: {company_name}\nThe report must strictly follow the requirements in the system prompt."

    response = await client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format=ResearchReport,
        temperature=0.25, # As requested
        max_tokens=6000, # As requested
    )

    return response.choices[0].message.parsed
