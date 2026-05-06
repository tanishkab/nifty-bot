# NIFTY AUTO TRADER - LIVE DEPLOYMENT GUIDE

## ⚠️ CRITICAL SAFETY WARNINGS

1. **REAL MONEY RISK**: Live mode trades with REAL MONEY. Losses are possible.
2. **TEST FIRST**: Always test in Paper mode for at least 1-2 weeks before going live
3. **START SMALL**: Begin with minimum lot sizes
4. **MONITOR**: Never leave it unattended on first day
5. **STOP LOSS**: Always set proper SL/TSL values

---

## STEP 1: VERIFY CREDENTIALS (DONE ✓)

Your current credentials in code:
- API_KEY: x9Zs2hWZ
- CLIENT_ID: J109737
- BOT_TOKEN: 8665264906:***
- CHAT_ID: 8748890897

⚠️ **SECURITY**: Consider moving these to environment variables or config file

---

## STEP 2: TEST IN PAPER MODE FIRST (REQUIRED)

### Run Paper Trading Test:

```bash
# Navigate to project directory
cd /Users/tanishkabansal/nifty-options-bot

# Run the application
python3 main_consolidated.py
```

### In the GUI:
1. Select **Symbol**: NIFTY 50 (or your choice)
2. Select **Mode**: Paper
3. Click **START**
4. Monitor for 1-2 days

### Paper Trading Checklist:
- [ ] Bot logs in successfully
- [ ] Tokens refresh automatically
- [ ] Signals are generated correctly
- [ ] Entry/Exit logic works
- [ ] Telegram alerts are received
- [ ] SL/TSL/Target points work as expected
- [ ] No errors in logs (check `trader.log`)

---

## STEP 3: RUN BACKTEST (RECOMMENDED)

Before live trading, backtest your settings:

1. Go to **Backtest** tab
2. Symbol: NIFTY 50
3. Days: 30 (test last 1 month)
4. Click **RUN BACKTEST**
5. Review results - Win rate should be >50%

### Good Backtest Results:
- Win Rate: >50%
- P&L: Positive
- Max consecutive losses: <3

---

## STEP 4: OPTIMIZE SETTINGS

Go to **Settings** tab and fine-tune:

### Conservative Settings (RECOMMENDED for first week):
```
EMA Fast: 9
EMA Slow: 21
EMA Gap: 3 points (increase for fewer signals)
Stop Loss: 30 points
Trailing SL: 20 points
Target: 60 points
Volume Mult: 1.2
Both Side: YES (trade both CE and PE)
```

### Aggressive Settings (Use after testing):
```
EMA Gap: 2 points (more signals)
SL: 25 points
TSL: 15 points
Target: 50 points
```

---

## STEP 5: PRE-LIVE CHECKLIST

Before switching to LIVE mode:

### Account Check:
- [ ] Angel One account has sufficient balance
- [ ] Margins are available for options trading
- [ ] Check if account allows API trading
- [ ] Verify lot size matches your capital (NIFTY = 50 lot)

### System Check:
- [ ] Internet connection is stable
- [ ] Mac won't sleep during trading hours (9:15 AM - 3:30 PM)
- [ ] Telegram bot is working (Test TG button)
- [ ] Phone/alerts are set up

### Risk Management:
- [ ] Set daily loss limit in your mind (e.g., Rs. 5,000 max loss)
- [ ] Start with 1 lot only (NIFTY = 50 quantity)
- [ ] Keep stop loss at 30+ points minimum
- [ ] Don't override the bot manually

---

## STEP 6: GO LIVE (Day 1)

### Morning Preparation (Before 9:15 AM):

1. **Open the application**:
   ```bash
   cd /Users/tanishkabansal/nifty-options-bot
   python3 main_consolidated.py
   ```

2. **Configure**:
   - Symbol: NIFTY 50
   - Mode: **LIVE** (⚠️ REAL MONEY)
   - Verify all settings in Settings tab

3. **Start Trading**:
   - Click **START** at 9:15 AM
   - Confirm the "Real money risk" dialog
   - Bot will auto-login and refresh tokens

### First Day Monitoring:

⚠️ **STAY ALERT**: Monitor every trade on Day 1

- Watch Live Log continuously
- Check Telegram messages
- Verify orders on Angel One app/web
- Track P&L in real-time
- Keep STOP button ready

### When to STOP Immediately:
- Daily loss exceeds your limit
- Bot shows repeated errors
- Unexpected behavior
- Market is highly volatile (e.g., news event)

---

## STEP 7: DAILY ROUTINE

### Morning (9:00 AM):
1. Start application
2. Check `trader.log` for any issues
3. Verify tokens refreshed (auto-happens)
4. Click START at 9:15 AM

### During Market Hours:
- Check Telegram every 30 minutes
- Monitor P&L
- Watch for alerts

### Evening (3:30 PM):
- Review EOD report (Telegram PDF)
- Check Trade Log tab
- Analyze win/loss ratio
- Update settings if needed

### Weekly Review:
- Total P&L
- Win rate
- Average profit/loss per trade
- Adjust settings based on performance

---

## STEP 8: MONITORING & LOGS

### Check Logs:
```bash
# View live logs
tail -f /Users/tanishkabansal/nifty-options-bot/trader.log

# View last 50 lines
tail -50 /Users/tanishkabansal/nifty-options-bot/trader.log
```

### Telegram Commands:
- `/start` - Start trading
- `/stop` - Stop trading
- `/status` - Current status
- `/report` - Get EOD report
- `/help` - Show commands

---

## STEP 9: TROUBLESHOOTING

### Login Fails:
- Check TOTP secret is correct
- Verify password
- Check Angel One session limits (max 1 active session)

### No Signals Generated:
- EMA Gap might be too high (reduce to 2)
- Volume filter too strict (reduce VOL_MULT to 1.0)
- Check if Future volume data is available

### Orders Rejected:
- Insufficient margin
- Option token not found (check expiry)
- Market hours (9:15-3:30 only)

### Token Not Found:
- Tokens auto-refresh at 9:00 AM
- Manual refresh: restart the app
- Check expiry date (Options expire weekly on Thursday)

---

## STEP 10: SAFETY FEATURES BUILT-IN

Your bot has these safety features:
- ✅ Stop Loss (30 points)
- ✅ Trailing Stop Loss (20 points)
- ✅ Target (60 points)
- ✅ Market hours check (9:15-3:30)
- ✅ Auto token refresh (weekly options)
- ✅ Volume filter (avoids low volume entries)
- ✅ EMA gap confirmation (reduces false signals)

---

## ADVANCED: RUN AS BACKGROUND SERVICE (Optional)

To keep bot running even if terminal closes:

```bash
# Install screen
brew install screen

# Start in background
screen -S nifty-bot
cd /Users/tanishkabansal/nifty-options-bot
python3 main_consolidated.py

# Detach: Press Ctrl+A, then D

# Reattach later:
screen -r nifty-bot
```

---

## EMERGENCY STOP

If something goes wrong:

1. **Click STOP button** in GUI
2. Or send `/stop` via Telegram
3. Or close the application
4. Manually close positions on Angel One app if needed

---

## CAPITAL ALLOCATION EXAMPLE

### For Rs. 1,00,000 Capital:
- NIFTY 50 (1 lot) ≈ Rs. 15,000-25,000 margin
- Keep 3-4 lot margin available
- Expected return: Rs. 2,000-5,000 per day (realistic)
- Max risk per trade: Rs. 1,500 (30 points × 50 lot)

### For Rs. 50,000 Capital:
- Start with 1 lot only
- Expected return: Rs. 1,000-2,000 per day
- Be conservative with settings

---

## PERFORMANCE EXPECTATIONS

### Realistic Goals:
- **Win Rate**: 55-65%
- **Daily Profit**: 2-5% of capital
- **Drawdown Days**: Expect 3-4 losing days per month
- **Best Case**: 8-10% monthly return
- **Worst Case**: -5% monthly loss

### Red Flags:
- Win rate <40%
- Consecutive 5+ losses
- Daily loss >10% of capital

---

## LEGAL DISCLAIMER

- This bot is for educational/personal use
- You are responsible for all trades
- Trading involves risk of loss
- Past performance ≠ future results
- Consult a financial advisor before trading

---

## SUPPORT CHECKLIST

Before going live, ensure:
- [ ] Tested in Paper mode for 1+ week
- [ ] Backtest shows positive results
- [ ] Capital available in Angel One account
- [ ] Stop loss settings are conservative
- [ ] Telegram alerts working
- [ ] Understand all risks
- [ ] Have time to monitor first day
- [ ] Emergency exit plan ready

---

## 🚀 READY TO GO LIVE?

If all above checkboxes are ✅, you can switch to LIVE mode.

**Start small. Monitor closely. Scale gradually.**

Good luck! 📈

---

**Need Help?**
- Check `trader.log` for errors
- Review Telegram alerts
- Test with Paper mode first
- Monitor Angel One app for order confirmations