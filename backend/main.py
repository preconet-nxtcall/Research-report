import os
import sys

# Add the root project directory to sys.path so 'backend' module can be imported when running directly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
from backend.services.ai_service import generate_research_report
from backend.services.export_service import generate_pdf, generate_docx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generated_reports = {}

@app.post("/api/generate")
async def generate_report(
    company_name: str = Form(...)
):
    if not company_name:
        raise HTTPException(status_code=400, detail="Company name is required.")

    # VERSION 2 INTEGRATION POINT: 
    # If upgrading from AI-simulated data to a real Financial API (like Tracxn, MCA, or Bloomberg),
    # You would make HTTP requests to those external APIs right here using the `company_name`,
    # map their JSON response to our `ResearchReport` Pydantic model, and bypass the `generate_research_report` call entirely!
    try:
        report = await generate_research_report(company_name)
        report_id = str(uuid.uuid4())
        generated_reports[report_id] = {
            "report": report,
            "company_name": company_name
        }
        
        return {"report_id": report_id, "report": report.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/pdf/{report_id}")
async def download_pdf(report_id: str):
    if report_id not in generated_reports:
        raise HTTPException(status_code=404, detail="Report not found")
    
    data = generated_reports[report_id]
    pdf_buffer = generate_pdf(data["report"], data["company_name"])
    
    return Response(
        content=pdf_buffer.read(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Research_Report_{report_id}.pdf"}
    )

@app.get("/api/download/docx/{report_id}")
async def download_docx(report_id: str):
    if report_id not in generated_reports:
        raise HTTPException(status_code=404, detail="Report not found")
        
    data = generated_reports[report_id]
    docx_buffer = generate_docx(data["report"], data["company_name"])
    
    return Response(
        content=docx_buffer.read(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=Research_Report_{report_id}.docx"}
    )

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
