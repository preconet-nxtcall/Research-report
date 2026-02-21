import os
from io import BytesIO
from backend.models import (
    ResearchReport, HistoricalFinancial, FinancialRatios, 
    PeerComparison, UnitEconomic, CapitalStructure, 
    ForwardProjection, ScorecardItem, SwotAnalysis,
    AssumptionSensitivity
)
from backend.services.export_service import generate_pdf, generate_docx

def test():
    # Mock data following the explicit new 17-key advanced institutional JSON schema
    report = ResearchReport(
        executiveSummary="Strong growth in AI sector.",
        businessOverviewAndMarketPositioning="Leading the market in generative tech.",
        historicalFinancialPerformance=[
            HistoricalFinancial(year="FY2023", revenueINR_cr=100.0, ebitdaINR_cr=20.0, patINR_cr=15.0, epsINR=5.0)
        ],
        financialRatiosAndValuationMetrics=FinancialRatios(peRatio=15.0, pbRatio=3.0, evToEbitda=10.0, evToSales=2.0, roePercent=20.0, rocePercent=18.0),
        peerComparisonAnalysis=[
            PeerComparison(company="Peer A", revenueINR_cr=120.0, evToEbitda=12.0, peRatio=18.0, revenueGrowthPercent=15.0, roePercent=15.0)
        ],
        unitEconomicsAndKPIs=[
            UnitEconomic(metric="CAC", value="INR 500")
        ],
        capitalStructureAndSecondaryOffer=CapitalStructure(
            totalSharesOutstanding_mn=10.0, promoterHoldingPercent=60.0, institutionalHoldingPercent=30.0, employeeHoldingPercent=10.0, indicativeValuationINR_cr=1000.0, secondaryOfferSizeINR_cr=100.0, impliedPerShareValueINR=100.0
        ),
        forwardProjections=[
            ForwardProjection(scenario="Base", revenueINR_cr=150.0, ebitdaMarginPercent=25.0, patINR_cr=30.0)
        ],
        exitPathwaysAndLiquidity="IPO in 24 months.",
        swotAnalysis=SwotAnalysis(
            strengths=["Strong tech"], weaknesses=["High burn rate"], opportunities=["Market expansion"], threats=["Regulation"]
        ),
        governanceComplianceAndRisk=["Indy Board"],
        investmentHighlightsAndThesis=["High growth."],
        investmentScorecard=[
            ScorecardItem(parameter="Growth Visibility", ratingOutOf5=4.5)
        ],
        investmentSizingAndMinimums="Min tick $50k",
        assumptionsAndSensitivityAnalysis=AssumptionSensitivity(
            entryValuationINR_cr=1000.0,
            exitValuationINR_cr=3000.0,
            holdingPeriod_years=5.0,
            baseCaseIRR_percent=25.0, 
            bullCaseIRR_percent=35.0, 
            bearCaseIRR_percent=10.0, 
            moic_base=3.5, 
            exitMultipleAssumption="15x EV/EBITDA", 
            valuationSensitivityCommentary="Highly sensitive to growth."
        ),
        dataRoomAndDueDiligenceChecklist=["Audited Financials 2021-2023"],
        nextStepsAndTransactionTimeline="Close by Q3.",
        assumptionsAndLimitations="This report uses AI-simulated data and is not investment advice."
    )
    
    # Test generation
    try:
        pdf_buffer = generate_pdf(report, "Mock Company")
        print(f"PDF Size: {len(pdf_buffer.getvalue())} bytes")
        
        docx_buffer = generate_docx(report, "Mock Company")
        print(f"DOCX Size: {len(docx_buffer.getvalue())} bytes")
        
        print("ALL TESTS PASSED: Both PDF and DOCX successfully generated using strict 17-KEY schema.")
    except Exception as e:
        print(f"FAILED: {str(e)}")

if __name__ == '__main__':
    test()
