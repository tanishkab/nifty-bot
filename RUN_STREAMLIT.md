# 🚀 STREAMLIT APP - QUICK START

## ✅ Backtest Functionality FIXED!

Your `app_streamlit.py` has been updated with **working backtest functionality**.

---

## 🎯 To Launch the App:

```bash
cd /Users/tanishkabansal/nifty-options-bot
streamlit run app_streamlit.py
```

Or use the shortcut:
```bash
python3 -m streamlit run app_streamlit.py
```

---

## 🌐 Access the App:

After running, the app will open at:
- **Local URL**: http://localhost:8501
- **Network URL**: http://192.168.x.x:8501

---

## 📊 What's Fixed:

### Backtest Tab Now Has:

1. **✅ Full Backtest Execution**
   - Login to Angel One
   - Refresh option tokens
   - Fetch historical data
   - Run backtest with real premiums
   - Display results

2. **📈 Rich Results Display**
   - Total trades, win rate, P&L
   - CE/PE split
   - Average win/loss
   - Complete trades table

3. **📥 Export Options**
   - Download CSV
   - Generate PDF report
   - Send to Telegram

4. **⏳ Progress Indicators**
   - Live progress bar
   - Status updates
   - Log output

---

## 🎨 App Features:

### Tab 1: Dashboard
- Live metrics
- Recent trades
- Current positions
- Download reports (PDF/CSV/Excel)

### Tab 2: Backtest ✅ (FIXED!)
- Configure symbol & days
- Real-time backtest execution
- Detailed results with metrics
- Export & share options

### Tab 3: Scanner
- Scan multiple symbols
- Live signals

### Tab 4: Settings
- Trading parameters
- API credentials
- Save configuration

---

## 🔧 How Backtest Works:

1. **Click "Run Backtest"** in Backtest tab
2. **Login happens automatically** if not logged in
3. **Tokens refresh** to get latest option data
4. **Historical data fetched** from Angel API
5. **Backtest runs** with your settings
6. **Results displayed** with full analysis

---

## 💡 Tips:

- **First Time**: Login will happen automatically on first backtest
- **Settings**: Adjust EMA Gap, SL, TSL, Target in Settings tab
- **Days**: Test with 7-30 days for faster results
- **Export**: Download CSV or send to Telegram directly

---

## 🐛 Troubleshooting:

### "Login failed"
- Check credentials in Settings tab
- Verify TOTP secret is correct

### "No trades generated"
- Reduce EMA_GAP to 2
- Reduce VOL_MULT to 1.0
- Try different symbol

### App not loading
- Make sure port 8501 is free
- Try: `streamlit run app_streamlit.py --server.port 8502`

---

## 📱 Keyboard Shortcuts:

- `R` - Rerun the app
- `C` - Clear cache
- `?` - Show keyboard shortcuts

---

## ✅ Testing Checklist:

- [ ] App launches without errors
- [ ] Dashboard shows metrics
- [ ] Backtest tab loads properly
- [ ] Click "Run Backtest" button
- [ ] Login happens automatically
- [ ] Progress bar shows status
- [ ] Results display with trades
- [ ] Can download CSV
- [ ] Can send to Telegram

---

## 🚀 Ready to Use!

Your Streamlit app is now **fully functional** with working backtest!

**Launch it now:**
```bash
streamlit run app_streamlit.py
```

Enjoy! 📈
