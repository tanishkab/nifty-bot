# 📊 Report Download Feature

## Overview

The Nifty Auto Trader web app now supports **3 report download formats**: PDF, CSV, and Excel.

## Download Locations

### Sidebar - Quick Actions

Located in the left sidebar under "Quick Actions":

1. **📄 PDF** - Professional formatted report with summary and trade log
2. **📊 CSV** - Spreadsheet format for Excel/Google Sheets
3. **📗 Excel** - Native .xlsx format with headers

Available only when trades exist for today.

### Dashboard Tab - All Trades

Located in Dashboard tab next to "Recent Trades" heading:

- **⬇️ All Trades CSV** - Download complete trade history (all dates)

## Report Contents

### PDF Report
- **Summary Section:**
  - Symbol, Mode, Total Trades
  - CE/PE trade breakdown
  - Win/Loss count and rate
  - Total P&L
  - Trading parameters (SL, TSL, Target, EMA Gap)

- **Trade Log Section:**
  - Entry/Exit timestamps
  - Option type (CE/PE)
  - Direction (Bull/Bear)
  - Strike price
  - Spot entry/exit
  - Option premium entry/exit
  - P&L per trade
  - Exit reason

### CSV Export
- All trade data in tabular format
- Columns: entry_time, otype, strike, spot_entry, opt_entry, opt_exit, pnl, reason
- Easy to import into Excel, Google Sheets, or data analysis tools
- Ideal for custom analysis and charting

### Excel Export
- Native .xlsx format
- Formatted with headers
- Ready for pivot tables and charts
- Compatible with Microsoft Excel, LibreOffice, Google Sheets

## File Naming Convention

- **PDF:** `report_YYYY-MM-DD.pdf` (e.g., `report_2026-05-06.pdf`)
- **CSV:** `trades_YYYY-MM-DD.csv` (e.g., `trades_2026-05-06.csv`)
- **Excel:** `trades_YYYY-MM-DD.xlsx` (e.g., `trades_2026-05-06.xlsx`)
- **All Trades:** `all_trades_YYYY-MM-DD.csv`

## Technical Implementation

### Functions

```python
generate_pdf_report(trades, symbol, mode)
# Returns: PDF bytes

generate_csv_report(trades)
# Returns: CSV string

generate_excel_report(trades)
# Returns: Excel bytes (openpyxl)
```

### Dependencies

```python
# PDF Generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Excel Generation
import openpyxl
```

### Streamlit Download Buttons

```python
st.download_button(
    label="📄 PDF",
    data=pdf_bytes,
    file_name=f"report_{datetime.date.today()}.pdf",
    mime="application/pdf",
    use_container_width=True
)
```

## Usage Examples

### 1. Daily Report Review
- Run backtest or paper trading
- Click "📄 PDF" in sidebar
- Review formatted report with charts and tables
- Share with team or save for records

### 2. Data Analysis
- Export trades as "📊 CSV"
- Open in Excel/Google Sheets
- Create pivot tables, charts
- Perform statistical analysis

### 3. Tax Records
- At end of trading day, download "📗 Excel"
- Maintain organized trade records
- Calculate P&L for tax filing
- Keep audit trail

### 4. Historical Analysis
- Click "⬇️ All Trades CSV" in Dashboard
- Get complete trade history across all dates
- Analyze long-term performance
- Identify patterns and improvements

## Benefits

✅ **Professional Reports** - PDF format for presentations and records
✅ **Data Portability** - CSV/Excel for custom analysis
✅ **No Manual Work** - Automated generation, instant download
✅ **Complete History** - All trades or filtered by date
✅ **Multiple Formats** - Choose based on use case
✅ **Browser Compatible** - Works in any modern browser
✅ **Mobile Friendly** - Download on phone/tablet

## Future Enhancements

Potential features for next version:

- [ ] Date range selector for custom period reports
- [ ] Charts/graphs embedded in PDF
- [ ] Email report automation
- [ ] Scheduled reports (daily, weekly)
- [ ] Multiple symbol comparison reports
- [ ] Risk metrics (Sharpe ratio, max drawdown)
- [ ] Trade journal with notes
- [ ] Performance attribution analysis

## Troubleshooting

**No download buttons visible:**
- Ensure you have trades for today
- Check that app is running properly
- Refresh browser if needed

**PDF empty or corrupt:**
- Check trades data exists in session state
- Review trader.log for errors
- Ensure reportlab is installed: `pip install reportlab`

**Excel won't open:**
- Ensure openpyxl is installed: `pip install openpyxl`
- Try opening with Google Sheets if Excel fails
- Check file size isn't zero bytes

**CSV garbled text:**
- Use UTF-8 encoding when opening
- In Excel: Data → From Text/CSV → UTF-8

## Support

For issues with report downloads:
1. Check browser console for errors
2. Review `trader.log` file
3. Ensure all dependencies installed: `pip install -r requirements.txt`
4. Try different browser if downloads fail
5. Report issues on GitHub

---

**Report Download Feature v1.0**
Added: May 6, 2026
