# ⚡ QUICK START GUIDE

## 🚀 To Start Trading (3 Steps)

### 1. Start the Application
```bash
cd /Users/tanishkabansal/nifty-options-bot
./start_trader.sh
```

Or directly:
```bash
python3 main_consolidated.py
```

### 2. Configure Settings
- **Symbol**: NIFTY 50 (or choose from dropdown)
- **Mode**:
  - 🧪 **Paper** - For testing (NO real money)
  - 📊 **Backtest** - Test historical data
  - 🔴 **LIVE** - Real money trading ⚠️

### 3. Click START
- Bot logs into Angel One
- Refreshes tokens automatically
- Starts monitoring signals
- Sends Telegram alerts

---

## 📱 Telegram Commands

Send these to your Telegram bot:
- `/start` - Start trading
- `/stop` - Stop trading
- `/status` - Check current status
- `/report` - Get today's report
- `/help` - Show commands

---

## ⚙️ Recommended Settings (Conservative)

```
EMA Fast: 9
EMA Slow: 21
EMA Gap: 3 points (fewer signals, safer)
Stop Loss: 30 points
Trailing SL: 20 points
Target: 60 points
Volume Period: 20
Volume Mult: 1.2
Both Side CE+PE: YES
```

---

## 🕐 Trading Schedule

- **9:00 AM** - Start application (tokens refresh)
- **9:15 AM** - Market opens, click START
- **3:30 PM** - Market closes, bot stops automatically
- **3:35 PM** - EOD report sent to Telegram

---

## 🛑 Emergency Stop

**If anything goes wrong:**
1. Click **STOP** button in GUI
2. Or send `/stop` on Telegram
3. Or close the application
4. Manually square off positions on Angel One app

---

## 📊 What to Monitor

### Live Log (GUI):
- ✅ Green = Signals, success
- 🔴 Red = Errors, losses
- 🟡 Yellow = Warnings
- 🔵 Blue = Info

### Key Events to Watch:
- `Login OK` - Angel One connected
- `Token refresh` - Option contracts updated
- `BUY CE/PE` - Trade entered
- `EXIT` - Trade closed
- `P&L: Rs.XXX` - Profit/Loss

---

## 💰 Risk Per Trade (NIFTY 50 = 50 lot)

| Stop Loss | Risk per Trade |
|-----------|----------------|
| 20 points | Rs. 1,000      |
| 30 points | Rs. 1,500      |
| 40 points | Rs. 2,000      |
| 50 points | Rs. 2,500      |

**Formula**: Risk = SL points × Lot Size (50 for Nifty)

---

## 🎯 Expected Performance

### Realistic Goals:
- **Win Rate**: 55-65%
- **Daily Profit**: Rs. 2,000-5,000 (1 lot)
- **Monthly Return**: 8-12% (good)
- **Losing Days**: 30-40% of days

### Warning Signs:
- Win rate <40% → Adjust settings
- 5 consecutive losses → Stop & review
- Daily loss >Rs. 5,000 → Stop for the day

---

## 📝 Daily Checklist

### Morning (Before 9:15 AM):
- [ ] Start application
- [ ] Check yesterday's log for errors
- [ ] Verify Angel One balance
- [ ] Set mode (Paper/Live)
- [ ] Click START

### During Trading (9:15-3:30):
- [ ] Check Telegram every 30 min
- [ ] Monitor P&L
- [ ] Watch for error alerts

### Evening (After 3:30):
- [ ] Review EOD PDF report
- [ ] Check win rate
- [ ] Note any issues
- [ ] Plan for tomorrow

---

## 🔧 Common Issues & Fixes

### "Login Failed"
- ✅ Check TOTP code (regenerate in Credentials tab)
- ✅ Verify password
- ✅ Check Angel One session limit

### "Token Not Found"
- ✅ Wait for 9:00 AM auto-refresh
- ✅ Restart application
- ✅ Check if options expired (Thursday)

### "No Signals Generated"
- ✅ Reduce EMA Gap to 2
- ✅ Lower Volume Mult to 1.0
- ✅ Check if market is open (9:15-3:30)

### "Order Rejected"
- ✅ Check margin available
- ✅ Verify lot size
- ✅ Check Angel One order limits

---

## 📂 Important Files

```
main_consolidated.py     → Main application
trader.log               → All logs (check for errors)
state.json               → Saved positions & balance
DEPLOYMENT_GUIDE.md      → Full deployment guide
PRE_LIVE_CHECKLIST.md    → Safety checklist
```

---

## 🔍 Where to Check Logs

```bash
# View last 50 lines
tail -50 trader.log

# Watch live
tail -f trader.log

# Search for errors
grep ERROR trader.log
```

---

## ⚠️ CRITICAL REMINDERS

1. **TEST FIRST**: Use Paper mode for 1-2 weeks
2. **START SMALL**: Begin with 1 lot only
3. **MONITOR**: Never leave unattended on Day 1
4. **STOP LOSS**: Always keep it at 30+ points
5. **DAILY LIMIT**: Set max loss per day (e.g., Rs. 5,000)
6. **MARKET HOURS**: Only 9:15 AM - 3:30 PM, Mon-Fri
7. **EXPIRY**: Options expire every Thursday 3:30 PM

---

## 🎓 Understanding the Strategy

### How It Works:
1. **EMA Crossover**: Fast EMA crosses Slow EMA
2. **Gap Confirmation**: Must have minimum gap (2-3 points)
3. **Volume Filter**: Current volume > 1.2× average
4. **Signal**: When all 3 conditions met → BUY CE or PE
5. **Exit**: When SL/TSL/Target hit or reverse signal

### Trade Example:
```
9:30 AM - EMA Fast crosses above EMA Slow with gap of 3 points
        → BUY CE (Call Option) at premium Rs. 150
        → Set SL: Rs. 120 (30 points below)
        → Set Target: Rs. 210 (60 points above)

10:15 AM - Premium reaches Rs. 180 (best so far)
         → TSL now at Rs. 160 (20 points below best)

10:45 AM - Premium hits Rs. 210 → TARGET HIT
         → EXIT with profit: Rs. 60 × 50 lot = Rs. 3,000
```

---

## 📞 Need Help?

1. Check `trader.log` for detailed errors
2. Read `DEPLOYMENT_GUIDE.md` for full guide
3. Review `PRE_LIVE_CHECKLIST.md` before going live
4. Test in Paper mode extensively
5. Monitor Telegram for real-time alerts

---

## ✅ Ready to Start?

```bash
# Quick start command:
cd /Users/tanishkabansal/nifty-options-bot && ./start_trader.sh
```

**Remember: Paper → Backtest → Live**

Good luck! 🚀📈
