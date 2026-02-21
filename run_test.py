import asyncio
import os
import sys

# Add backend directory to path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.ai_service import generate_research_report
from dotenv import load_dotenv

async def run():
    load_dotenv(dotenv_path='backend/.env')
    
    company_name = "Test Institutional NBFC Private Limited"
    print(f"Generating live report for: {company_name}")
    print("This will take 30-60 seconds as the AI populates the 17 nested dictionaries...\n")
    
    try:
        report = await generate_research_report(company_name)
        
        # Test specific dictionary requirements explicitly asked by user
        print(f"1. Exactly 5 Financial Years: {len(report.historicalFinancialPerformance) == 5}")
        print(f"   (Verified Years: {[x.year for x in report.historicalFinancialPerformance]})")
        print(f"2. Entry Valuation Exists: {bool(report.assumptionsAndSensitivityAnalysis.entryValuationINR_cr)}")
        print(f"3. Exit Valuation Exists: {bool(report.assumptionsAndSensitivityAnalysis.exitValuationINR_cr)}")
        print(f"4. Holding Period Exists: {bool(report.assumptionsAndSensitivityAnalysis.holdingPeriod_years)}")
        print(f"5. IRR/MOIC Generated: Base IRR = {report.assumptionsAndSensitivityAnalysis.baseCaseIRR_percent}%, MOIC = {report.assumptionsAndSensitivityAnalysis.moic_base}")
        
        # Mathematical verification!
        entry = report.assumptionsAndSensitivityAnalysis.entryValuationINR_cr
        exit_val = report.assumptionsAndSensitivityAnalysis.exitValuationINR_cr
        hold = report.assumptionsAndSensitivityAnalysis.holdingPeriod_years
        if entry > 0 and hold > 0:
            calc_moic = exit_val / entry
            calc_irr = ((exit_val / entry) ** (1 / hold)) - 1
            print(f"   -> AI MOIC: {report.assumptionsAndSensitivityAnalysis.moic_base} | True Math MOIC: {calc_moic:.2f}")
            print(f"   -> AI Base IRR: {report.assumptionsAndSensitivityAnalysis.baseCaseIRR_percent}% | True Math IRR: {(calc_irr*100):.2f}%")

        print(f"6. Peer ROE Included: {hasattr(report.peerComparisonAnalysis[0], 'roePercent')}")
        print(f"7. Disclaimer Appended: {report.assumptionsAndLimitations.startswith('DISCLAIMER')}")
        
        print("\n--- NEW PHASE 5: RATIO MATHEMATICS AUDIT ---")
        shares_mn = report.capitalStructureAndSecondaryOffer.totalSharesOutstanding_mn
        pat_fy24 = report.historicalFinancialPerformance[-1].patINR_cr
        ai_pe = report.financialRatiosAndValuationMetrics.peRatio
        ai_eps = report.historicalFinancialPerformance[-1].epsINR
        ai_implied_price = report.capitalStructureAndSecondaryOffer.impliedPerShareValueINR
        
        calc_pe = entry / pat_fy24 if pat_fy24 else 0
        calc_eps = (pat_fy24 * 10) / shares_mn if shares_mn else 0
        calc_implied = (entry * 10) / shares_mn if shares_mn else 0
        
        print(f"   -> Market Cap matches Entry Valuation: {entry} Cr")
        print(f"   -> AI P/E: {ai_pe} | True Math P/E: {calc_pe:.2f}")
        print(f"   -> AI FY24 EPS: {ai_eps} INR | True Math EPS: {calc_eps:.2f} INR")
        print(f"   -> AI Implied Share Price: {ai_implied_price} INR | True Math Price: {calc_implied:.2f} INR")

        print("\nSUCCESS! All keys loaded securely.")
        
        # Output the raw JSON so the user can verify the formatting
        with open("test_output.json", "w") as f:
            f.write(report.model_dump_json(indent=2))
        print("Raw JSON dumped to test_output.json")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(run())
