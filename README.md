# 📈 Nifty Auto Trader - Desktop & Web

Fully automatic trading bot for Nifty options with EMA crossover strategy. Available as Desktop (Tkinter) and Web (Streamlit) versions.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Desktop App
```bash
python main_consolidated.py
```

### 3. Run Web App
```bash
streamlit run app_streamlit.py
```

Access web version at `http://localhost:8501`

## ✨ Features

- ✅ **3 Trading Modes** - Backtest, Paper (simulation), Live
- 📊 **Download Reports** - PDF, CSV, Excel formats (NEW!)
- 🔄 **Auto Token Refresh** - Future (monthly) & Options (weekly)
- 📈 **EMA Strategy** - 9/21 EMA crossover with volume confirmation
- 🎯 **Risk Management** - Stop Loss, Trailing SL, Target points
- 📡 **Real-time Data** - Live market data from Angel One API
- 📱 **Telegram Alerts** - Real-time trade notifications
- 🌐 **Web Interface** - Access from anywhere (Streamlit)

## 📥 Download Reports (NEW!)

The web app now supports **3 download formats**:

### 1. PDF Report 📄
- Professional formatted report with summary stats
- Trade log with entry/exit details
- Win rate, P&L analysis
- **Location:** Sidebar → Quick Actions → "📄 PDF"

### 2. CSV Export 📊
- Simple spreadsheet format
- Easy to import into Excel/Google Sheets
- All trade data in tabular format
- **Location:** Sidebar → Quick Actions → "📊 CSV"

### 3. Excel Export 📗
- Native Excel format (.xlsx)
- Formatted with headers
- Ready for analysis
- **Location:** Sidebar → Quick Actions → "📗 Excel"

**Also Available:**
- Dashboard Tab → Recent Trades → "⬇️ All Trades CSV"

## 🌐 Deploy to Web (FREE)

### Quick Deploy on Streamlit Cloud

1. **Push to GitHub:**
```bash
git add .
git commit -m "Deploy web app"
git push origin main
```

2. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app" → Select repo → Deploy
   - Main file: `app_streamlit.py`

Your bot will be live at: `https://yourapp.streamlit.app`

See [DEPLOY.md](DEPLOY.md) for full deployment guide (VPS, Docker, etc.)

## 📈 Trading Strategy

**Entry Signal:**
- EMA 9 crosses above/below EMA 21
- Gap > 2 points confirmed
- Volume > 1.2x average (from Nifty Future)
- Buy ATM Call (CE) on bullish / Put (PE) on bearish

**Exit Conditions:**
- Stop Loss: -30 points from entry
- Trailing SL: -20 points from best price
- Target: +60 points from entry
- Reverse signal (CE→PE or PE→CE)

**Instruments:** NIFTY, BANKNIFTY, FINNIFTY + stocks

## 🎮 GUI Tabs

### Desktop App (Tkinter)
1. **Trading** - Start/Stop, select symbol and mode
2. **Backtest** - Test on historical data
3. **Scanner** - Multi-instrument signal scanning
4. **Trades** - View trade history and P&L
5. **Settings** - Adjust EMA, SL, TSL, Target values
6. **Credentials** - Update API keys

### Web App (Streamlit)
1. **Dashboard** - Live monitoring, metrics, positions
2. **Backtest** - Historical testing with results
3. **Scanner** - Real-time signal scanning
4. **Settings** - Configure parameters and credentials

## ⚙️ Configuration

Customize in Settings tab or edit `main_consolidated.py` CFG:
```python
"EMA_FAST":   9,      # Fast EMA period
"EMA_SLOW":   21,     # Slow EMA period
"EMA_GAP":    2,      # Min gap for signal (points)
"SL_PTS":     30,     # Stop loss (points)
"TSL_PTS":    20,     # Trailing SL (points)
"TGT_PTS":    60,     # Target (points)
"VOL_PERIOD": 20,     # Volume average period
"VOL_MULT":   1.2,    # Volume multiplier
"PAPER_CAP":  100000, # Paper trading capital
```

## 📱 Telegram Commands

Send to your bot:
- `/start` - Start trading
- `/stop` - Stop trading
- `/status` - Current status & P&L
- `/report` - Download today's report
- `/help` - Show all commands

## 🔒 Security

**Never commit credentials!** Use environment variables:

```bash
# Create .env file (gitignored)
API_KEY=your_key
CLIENT_ID=your_id
PASSWORD=your_password
TOTP=your_totp_secret
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
```

On Streamlit Cloud, add secrets in Settings → Secrets.

## 📋 Requirements

```
Python 3.9+
pyotp
requests
pandas
numpy
reportlab
streamlit
plotly
openpyxl
smartapi-python
```

## 🛠️ Project Structure

```
nifty-options-bot/
├── main_consolidated.py    # Desktop app (Tkinter)
├── app_streamlit.py         # Web app (Streamlit)
├── requirements.txt         # Python dependencies
├── DEPLOY.md               # Deployment guide
├── README.md               # This file
├── state.json              # Auto-saved state
└── trader.log              # Trading logs
```

## 🔥 Safety Features

⚠️ **Default mode is PAPER (safe, no real orders)**

- Live mode requires manual confirmation
- Built-in risk management (SL/TSL/Target)
- Auto token refresh prevents stale data
- Comprehensive logging for audit
- Test thoroughly in Paper mode first

## 🐛 Troubleshooting

**macOS Tkinter Error:**
```bash
brew install python@3.13
/opt/homebrew/bin/python3.13 main_consolidated.py
```

**Login Failed:** Check Angel One credentials and TOTP secret

**No Trades:** Adjust EMA_GAP, volume settings, or try different symbols

**Web App Won't Start:**
```bash
streamlit cache clear
pip install --upgrade streamlit
```

**Check Logs:** See `trader.log` for detailed error messages

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/nifty-options-bot/issues)
- **Logs:** Check `trader.log` for debugging
- **Documentation:** See [DEPLOY.md](DEPLOY.md) for deployment help

## ⚠️ Disclaimer

This is educational software. Real trading involves risk of loss. Test thoroughly in paper mode before going live. Not financial advice. Use at your own risk.

## 📄 License

MIT License

---

**Made with ❤️ for algorithmic traders**

**Star ⭐ this repo if you find it useful!**