document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('generate-form');
    const submitBtn = document.getElementById('generate-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = document.getElementById('btn-loader');
    const loadingMessage = document.getElementById('loading-message');
    const errorMessage = document.getElementById('error-message');

    const resultSection = document.getElementById('result-section');
    const reportContainer = document.getElementById('report-container');
    const displayCompanyName = document.getElementById('display-company-name');

    const downloadPdfBtn = document.getElementById('download-pdf');
    const downloadDocxBtn = document.getElementById('download-docx');

    let currentReportId = null;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const companyName = document.getElementById('company_name').value.trim();

        if (!companyName) return;

        // Reset UI
        errorMessage.classList.add('hidden');
        resultSection.classList.add('hidden');
        loadingMessage.classList.remove('hidden');
        submitBtn.disabled = true;
        btnText.textContent = 'Processing...';
        btnLoader.classList.remove('hidden');

        try {
            const formData = new FormData();
            formData.append('company_name', companyName);

            const response = await fetch('/api/generate', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to generate report');
            }

            currentReportId = data.report_id;
            displayCompanyName.textContent = companyName;
            renderReport(data.report);

            resultSection.classList.remove('hidden');
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.classList.remove('hidden');
        } finally {
            submitBtn.disabled = false;
            btnText.textContent = 'GENERATE RESEARCH REPORT';
            btnLoader.classList.add('hidden');
            loadingMessage.classList.add('hidden');
        }
    });

    downloadPdfBtn.addEventListener('click', () => {
        if (!currentReportId) return;
        window.location.href = `/api/download/pdf/${currentReportId}`;
    });

    downloadDocxBtn.addEventListener('click', () => {
        if (!currentReportId) return;
        window.location.href = `/api/download/docx/${currentReportId}`;
    });

    function createCollapsibleSection(title, contentHtml, isOpen = false) {
        const id = 'section-' + Math.random().toString(36).substr(2, 9);
        const activeClass = isOpen ? 'active' : '';
        const displayStyle = isOpen ? 'max-height: 2000px;' : '';

        return `
            <div class="report-section">
                <button class="section-header ${activeClass}" aria-expanded="${isOpen}" aria-controls="${id}">
                    ${title}
                </button>
                <div class="section-content" id="${id}" style="${displayStyle}">
                    <div class="section-content-inner">
                        ${contentHtml}
                    </div>
                </div>
            </div>
        `;
    }

    function generateListHtml(items) {
        if (!items || items.length === 0) return '';
        let html = '<ul>';
        items.forEach(item => {
            html += `<li>${escapeHtml(item)}</li>`;
        });
        html += '</ul>';
        return html;
    }

    function formatText(text) {
        if (!text) return '';
        return `<p>${escapeHtml(text).replace(/\\n/g, '<br>')}</p>`;
    }

    function buildTableHtml(headers, rows) {
        let html = '<div style="overflow-x: auto;"><table class="data-table"><thead><tr>';
        headers.forEach(h => html += `<th>${escapeHtml(h)}</th>`);
        html += '</tr></thead><tbody>';
        rows.forEach(r => {
            html += '<tr>';
            r.forEach(c => html += `<td>${escapeHtml(c)}</td>`);
            html += '</tr>';
        });
        html += '</tbody></table></div>';
        return html;
    }

    function escapeHtml(unsafe) {
        return (unsafe || '').toString()
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function formatNumber(num) {
        if (num === null || num === undefined) return '';
        if (typeof num === 'number') {
            return new Intl.NumberFormat('en-IN', { maximumFractionDigits: 2 }).format(num);
        }
        return escapeHtml(num);
    }

    function renderReport(report) {
        let html = '';

        // 1. Executive Summary
        html += createCollapsibleSection("1. EXECUTIVE SUMMARY", formatText(report.executiveSummary), true);

        // 2. Business Overview
        html += createCollapsibleSection("2. BUSINESS OVERVIEW & MARKET POSITIONING", formatText(report.businessOverviewAndMarketPositioning), true);

        // 3. Historical Financials
        let histHeaders = ["Year", "Revenue (INR Cr)", "EBITDA (INR Cr)", "PAT (INR Cr)", "EPS (INR)"];
        let histRows = report.historicalFinancialPerformance.map(item => [
            item.year, formatNumber(item.revenueINR_cr), formatNumber(item.ebitdaINR_cr), formatNumber(item.patINR_cr), formatNumber(item.epsINR)
        ]);
        html += createCollapsibleSection("3. HISTORICAL FINANCIAL PERFORMANCE", buildTableHtml(histHeaders, histRows));

        // 4. Financial Ratios
        let ratioHeaders = ["P/E", "P/B", "EV/EBITDA", "EV/Sales", "ROE (%)", "ROCE (%)"];
        let ratioRows = [[
            formatNumber(report.financialRatiosAndValuationMetrics.peRatio),
            formatNumber(report.financialRatiosAndValuationMetrics.pbRatio),
            formatNumber(report.financialRatiosAndValuationMetrics.evToEbitda),
            formatNumber(report.financialRatiosAndValuationMetrics.evToSales),
            formatNumber(report.financialRatiosAndValuationMetrics.roePercent),
            formatNumber(report.financialRatiosAndValuationMetrics.rocePercent)
        ]];
        html += createCollapsibleSection("4. FINANCIAL RATIOS & VALUATION METRICS", buildTableHtml(ratioHeaders, ratioRows));

        // 5. Peer Comparison
        let peerHeaders = ["Company", "Revenue (INR Cr)", "EV/EBITDA", "P/E Ratio", "Rev Growth (%)", "ROE (%)"];
        let peerRows = report.peerComparisonAnalysis.map(p => [
            p.company, formatNumber(p.revenueINR_cr), formatNumber(p.evToEbitda), formatNumber(p.peRatio), formatNumber(p.revenueGrowthPercent), formatNumber(p.roePercent)
        ]);
        html += createCollapsibleSection("5. PEER COMPARISON ANALYSIS", buildTableHtml(peerHeaders, peerRows));

        // 6. Unit Economics
        let econHeaders = ["Metric", "Value"];
        let econRows = report.unitEconomicsAndKPIs.map(u => [u.metric, u.value]);
        html += createCollapsibleSection("6. UNIT ECONOMICS & KPIs", buildTableHtml(econHeaders, econRows));

        // 7. Capital Structure
        let cap = report.capitalStructureAndSecondaryOffer;
        let capHeaders = ["Detail", "Value"];
        let capRows = [
            ["Total Shares Outstanding (mn)", formatNumber(cap.totalSharesOutstanding_mn)],
            ["Promoter Holding (%)", formatNumber(cap.promoterHoldingPercent)],
            ["Institutional Holding (%)", formatNumber(cap.institutionalHoldingPercent)],
            ["Employee Holding (%)", formatNumber(cap.employeeHoldingPercent)],
            ["Indicative Valuation (INR Cr)", formatNumber(cap.indicativeValuationINR_cr)],
            ["Secondary Offer Size (INR Cr)", formatNumber(cap.secondaryOfferSizeINR_cr)],
            ["Implied Per Share Value (INR)", formatNumber(cap.impliedPerShareValueINR)]
        ];
        html += createCollapsibleSection("7. CAPITAL STRUCTURE & SECONDARY OFFER", buildTableHtml(capHeaders, capRows));

        // 8. Forward Projections
        let projHeaders = ["Scenario", "Revenue (INR Cr)", "EBITDA Margin (%)", "PAT (INR Cr)"];
        let projRows = report.forwardProjections.map(p => [
            p.scenario, formatNumber(p.revenueINR_cr), formatNumber(p.ebitdaMarginPercent), formatNumber(p.patINR_cr)
        ]);
        html += createCollapsibleSection("8. FORWARD PROJECTIONS", buildTableHtml(projHeaders, projRows));

        // 9. Exit Pathways
        html += createCollapsibleSection("9. EXIT PATHWAYS & LIQUIDITY", formatText(report.exitPathwaysAndLiquidity));

        // 10. SWOT Analysis
        let swotHtml = `
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4 style="margin-bottom:8px; color:#1e293b;">Strengths</h4>
                    ${generateListHtml(report.swotAnalysis.strengths)}
                </div>
                <div>
                    <h4 style="margin-bottom:8px; color:#1e293b;">Weaknesses</h4>
                    ${generateListHtml(report.swotAnalysis.weaknesses)}
                </div>
                <div>
                    <h4 style="margin-bottom:8px; color:#1e293b;">Opportunities</h4>
                    ${generateListHtml(report.swotAnalysis.opportunities)}
                </div>
                <div>
                    <h4 style="margin-bottom:8px; color:#1e293b;">Threats</h4>
                    ${generateListHtml(report.swotAnalysis.threats)}
                </div>
            </div>
        `;
        html += createCollapsibleSection("10. SWOT ANALYSIS", swotHtml);

        // 11. Governance & Risk
        html += createCollapsibleSection("11. GOVERNANCE, COMPLIANCE & RISK", generateListHtml(report.governanceComplianceAndRisk));

        // 12. Investment Highlights
        html += createCollapsibleSection("12. INVESTMENT HIGHLIGHTS & THESIS", generateListHtml(report.investmentHighlightsAndThesis));

        // 13. Scorecard
        let scoreHeaders = ["Parameter", "Rating (/5)"];
        let scoreRows = report.investmentScorecard.map(s => [s.parameter, formatNumber(s.ratingOutOf5)]);
        html += createCollapsibleSection("13. INVESTMENT SCORECARD", buildTableHtml(scoreHeaders, scoreRows));

        // 14. Minimums
        html += createCollapsibleSection("14. INVESTMENT SIZING & MINIMUMS", formatText(report.investmentSizingAndMinimums));

        // 15. Sensitivity Assumptions
        let sens = report.assumptionsAndSensitivityAnalysis;
        let sensHeaders = ["Parameter", "Assumption Value"];
        let sensRows = [
            ["Entry Valuation (INR Cr)", formatNumber(sens.entryValuationINR_cr)],
            ["Exit Valuation (INR Cr)", formatNumber(sens.exitValuationINR_cr)],
            ["Holding Period (Years)", formatNumber(sens.holdingPeriod_years)],
            ["Base Case IRR (%)", formatNumber(sens.baseCaseIRR_percent)],
            ["Bull Case IRR (%)", formatNumber(sens.bullCaseIRR_percent)],
            ["Bear Case IRR (%)", formatNumber(sens.bearCaseIRR_percent)],
            ["MOIC (Base)", formatNumber(sens.moic_base)],
            ["Exit Multiple Assumption", sens.exitMultipleAssumption]
        ];
        let sensHtml = buildTableHtml(sensHeaders, sensRows) + `<div style="margin-top:15px; border-top: 1px dotted #ccc; padding-top: 10px;"><strong>Valuation Commentary:</strong><br>${formatText(sens.valuationSensitivityCommentary)}</div>`;
        html += createCollapsibleSection("15. VALUATION SENSITIVITY & ASSUMPTIONS", sensHtml);

        // 16. Data Room
        html += createCollapsibleSection("16. DATA ROOM & DUE DILIGENCE", generateListHtml(report.dataRoomAndDueDiligenceChecklist));

        // 17. Timeline and Limitations
        html += createCollapsibleSection("17. NEXT STEPS & TIMELINE", formatText(report.nextStepsAndTransactionTimeline));
        html += createCollapsibleSection("18. ASSUMPTIONS & LIMITATIONS", formatText(report.assumptionsAndLimitations));


        reportContainer.innerHTML = html;

        // Attach event listeners to collapsible headers
        const collapsibles = reportContainer.querySelectorAll('.section-header');
        collapsibles.forEach(btn => {
            btn.addEventListener('click', function () {
                this.classList.toggle('active');
                const content = this.nextElementSibling;
                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                } else {
                    content.style.maxHeight = content.scrollHeight + "px";
                }
            });
        });
    }
});
