# 🚀 Quick Reference Card

## Run Commands

```bash
# Desktop App
python main_consolidated.py

# Web App
streamlit run app_streamlit.py
```

## Download Reports

| Format | Button | Location | Use Case |
|--------|--------|----------|----------|
| PDF | 📄 PDF | Sidebar → Quick Actions | Professional reports, printing |
| CSV | 📊 CSV | Sidebar → Quick Actions | Excel analysis, data export |
| Excel | 📗 Excel | Sidebar → Quick Actions | Native Excel files, pivot tables |
| All Trades | ⬇️ All Trades CSV | Dashboard → Recent Trades | Complete history |

## File Names

- `report_2026-05-06.pdf` - Today's PDF report
- `trades_2026-05-06.csv` - Today's CSV export
- `trades_2026-05-06.xlsx` - Today's Excel export
- `all_trades_2026-05-06.csv` - Complete trade history

## Report Contents

### PDF Report
- Summary stats (trades, win rate, P&L)
- Trade log with timestamps
- Entry/exit prices
- SL/TSL/Target settings

### CSV/Excel
- entry_time
- otype (CE/PE)
- strike
- spot_entry
- opt_entry
- opt_exit
- pnl
- reason

## Quick Deploy

```bash
# 1. Push to GitHub
git add .
git commit -m "Add web app"
git push origin main

# 2. Deploy on Streamlit Cloud
# Go to: share.streamlit.io
# Click: New app → Select repo → Deploy
```

## Settings Quick Reference

| Setting | Default | Range | Purpose |
|---------|---------|-------|---------|
| EMA_FAST | 9 | 5-20 | Fast moving average |
| EMA_SLOW | 21 | 15-50 | Slow moving average |
| EMA_GAP | 2 | 1-5 | Min gap for signal |
| SL_PTS | 30 | 20-100 | Stop loss points |
| TSL_PTS | 20 | 10-50 | Trailing SL points |
| TGT_PTS | 60 | 30-200 | Target points |
| VOL_MULT | 1.2 | 1.0-2.0 | Volume multiplier |

## Telegram Commands

```
/start  - Start trading
/stop   - Stop trading
/status - Show current status
/report - Send today's report
/help   - Show all commands
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No download buttons | Ensure trades exist for today |
| PDF won't open | Install reportlab: `pip install reportlab` |
| Excel won't open | Install openpyxl: `pip install openpyxl` |
| Web app won't start | `streamlit cache clear` |
| Login failed | Check API credentials |

## Support

- **Logs:** `trader.log`
- **Docs:** `README.md`, `FEATURES.md`
- **Deploy:** `DEPLOY.md`
- **Summary:** `SUMMARY.md`

---

**Version 2.0 | Report Downloads Enabled ✅**
