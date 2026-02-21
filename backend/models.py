from pydantic import BaseModel, field_validator
from typing import List, Literal

class HistoricalFinancial(BaseModel):
    year: Literal["FY2020", "FY2021", "FY2022", "FY2023", "FY2024"]
    revenueINR_cr: float
    ebitdaINR_cr: float
    patINR_cr: float
    epsINR: float

class FinancialRatios(BaseModel):
    peRatio: float
    pbRatio: float
    evToEbitda: float
    evToSales: float
    roePercent: float
    rocePercent: float

class PeerComparison(BaseModel):
    company: str
    revenueINR_cr: float
    evToEbitda: float
    peRatio: float
    revenueGrowthPercent: float
    roePercent: float

class UnitEconomic(BaseModel):
    metric: str
    value: str

class CapitalStructure(BaseModel):
    totalSharesOutstanding_mn: float
    promoterHoldingPercent: float
    institutionalHoldingPercent: float
    employeeHoldingPercent: float
    indicativeValuationINR_cr: float
    secondaryOfferSizeINR_cr: float
    impliedPerShareValueINR: float

class ForwardProjection(BaseModel):
    scenario: str
    revenueINR_cr: float
    ebitdaMarginPercent: float
    patINR_cr: float

class SwotAnalysis(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]

class ScorecardItem(BaseModel):
    parameter: str
    ratingOutOf5: float

class AssumptionSensitivity(BaseModel):
    entryValuationINR_cr: float
    exitValuationINR_cr: float
    holdingPeriod_years: float
    baseCaseIRR_percent: float
    bullCaseIRR_percent: float
    bearCaseIRR_percent: float
    moic_base: float
    exitMultipleAssumption: str
    valuationSensitivityCommentary: str

from pydantic import BaseModel, field_validator

class ResearchReport(BaseModel):
    executiveSummary: str
    businessOverviewAndMarketPositioning: str
    historicalFinancialPerformance: List[HistoricalFinancial]
    financialRatiosAndValuationMetrics: FinancialRatios
    peerComparisonAnalysis: List[PeerComparison]
    unitEconomicsAndKPIs: List[UnitEconomic]
    capitalStructureAndSecondaryOffer: CapitalStructure
    forwardProjections: List[ForwardProjection]
    exitPathwaysAndLiquidity: str
    swotAnalysis: SwotAnalysis
    governanceComplianceAndRisk: List[str]
    investmentHighlightsAndThesis: List[str]
    investmentScorecard: List[ScorecardItem]
    investmentSizingAndMinimums: str
    assumptionsAndSensitivityAnalysis: AssumptionSensitivity
    dataRoomAndDueDiligenceChecklist: List[str]
    nextStepsAndTransactionTimeline: str
    assumptionsAndLimitations: str
    
    @field_validator('assumptionsAndLimitations')
    @classmethod
    def prepend_disclaimer(cls, v: str) -> str:
        disclaimer_text = "DISCLAIMER: This report uses AI-simulated data for illustrative research only. It does not use real-time market data and is not investment advice. "
        if not v.startswith("DISCLAIMER"):
            return disclaimer_text + v
        return v
