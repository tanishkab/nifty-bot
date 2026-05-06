run # PRE-LIVE DEPLOYMENT CHECKLIST

## 📋 Complete this checklist BEFORE going LIVE

Date: _______________

---

## PHASE 1: PAPER TRADING TEST (Required: 1-2 weeks)

### Week 1 Testing:
- [ ] Day 1: Bot started successfully in PAPER mode
- [ ] Day 2: Signals generated correctly
- [ ] Day 3: Entry/Exit logic working
- [ ] Day 4: Telegram alerts received
- [ ] Day 5: Stop loss working correctly

### Results Review:
- Total Paper Trades: _______
- Win Rate: _______% (Should be >50%)
- Total P&L: Rs. _______
- Max Loss in Single Trade: Rs. _______
- Any Errors? (check trader.log): _______

**Decision**:
- [ ] Results are acceptable → Proceed to Phase 2
- [ ] Results need improvement → Continue testing

---

## PHASE 2: BACKTEST ANALYSIS

### Run Backtest for Last 30 Days:
- Symbol: NIFTY 50
- Days: 30
- Results:
  - Total Trades: _______
  - Win Rate: _______% (Should be >50%)
  - Total P&L: Rs. _______
  - Max Drawdown: Rs. _______

**Decision**:
- [ ] Backtest positive → Proceed
- [ ] Backtest negative → Adjust settings and retest

---

## PHASE 3: TECHNICAL CHECKLIST

### System Verification:
- [ ] Python 3.9+ installed
- [ ] All packages installed (run `pip3 list`)
- [ ] Mac will stay awake during market hours (9:15 AM - 3:30 PM)
- [ ] Internet connection is stable (>10 Mbps)
- [ ] Backup internet available (mobile hotspot)
- [ ] Power backup available (laptop battery/UPS)

### Application Check:
- [ ] `main_consolidated.py` runs without errors
- [ ] GUI opens properly
- [ ] All tabs visible (Trading, Backtest, Scanner, Trades, Settings, Credentials)
- [ ] Can switch between modes (paper/live/backtest)
- [ ] Logs are writing to `trader.log`

### Angel One Account:
- [ ] Account is active and operational
- [ ] Sufficient balance available: Rs. _______
- [ ] Options trading enabled
- [ ] API access enabled
- [ ] TOTP authentication working
- [ ] Can place manual order via app (test)

### Credentials Verification:
- [ ] API Key is correct: `x9Zs2hWZ`
- [ ] Client ID is correct: `J109737`
- [ ] Password is correct (test login manually)
- [ ] TOTP generating correct codes
- [ ] Login succeeds in application

### Telegram Setup:
- [ ] Bot token is valid
- [ ] Chat ID is correct
- [ ] Test message received (click "Test TG" button)
- [ ] Voice alerts working (optional)
- [ ] Phone notifications enabled for Telegram

---

## PHASE 4: SETTINGS OPTIMIZATION

### Current Settings (Review and Confirm):

**EMA Settings:**
- EMA Fast: _______ (recommended: 9)
- EMA Slow: _______ (recommended: 21)
- EMA Gap: _______ pts (recommended: 2-3)

**Risk Management:**
- Stop Loss: _______ pts (recommended: 30+)
- Trailing SL: _______ pts (recommended: 20)
- Target: _______ pts (recommended: 60)

**Volume Filter:**
- Volume Period: _______ (recommended: 20)
- Volume Multiplier: _______ (recommended: 1.2)

**Trading Options:**
- [ ] Both Side CE+PE enabled
- [ ] Voice alerts enabled/disabled

**Capital:**
- Paper Capital: Rs. _______ (for testing)
- Actual Capital Available: Rs. _______
- Max Risk Per Trade: Rs. _______ (SL pts × lot size)

---

## PHASE 5: RISK ASSESSMENT

### Capital & Risk:
- Available Capital: Rs. _______
- Max Daily Loss Limit: Rs. _______ (set 5-10% of capital)
- Position Size: _______ lots (start with 1 lot)
- Margin Required per Lot: Rs. _______ (check Angel One)

### Emergency Plan:
- [ ] Know how to STOP bot immediately (Stop button)
- [ ] Can send `/stop` via Telegram
- [ ] Know how to close positions manually on Angel One app
- [ ] Have Angel One customer care number saved

### Monitoring Plan:
- [ ] Will monitor continuously on Day 1
- [ ] Telegram notifications enabled
- [ ] Trading hours blocked in calendar (9:15 AM - 3:30 PM)
- [ ] Laptop/Mac will be available during market hours

---

## PHASE 6: KNOWLEDGE CHECK

Answer these questions to ensure you understand:

1. **What does EMA Gap = 3 mean?**
   Answer: __________________________________________

2. **When does the bot stop a trade?**
   Answer: __________________________________________

3. **What happens when weekly options expire (Thursday)?**
   Answer: __________________________________________

4. **How much can you lose in one trade with 1 lot and 30 point SL?**
   Answer: Rs. ________ (Hint: 30 × 50 = Rs. 1,500)

5. **What will you do if bot shows repeated errors?**
   Answer: __________________________________________

---

## PHASE 7: FINAL GO/NO-GO DECISION

### Paper Trading Results:
- [ ] ✅ Win rate >50%
- [ ] ✅ Profitable over 1-2 weeks
- [ ] ✅ No critical errors in logs
- [ ] ✅ Telegram alerts working

### Backtest Results:
- [ ] ✅ Positive P&L over 30 days
- [ ] ✅ Win rate >50%
- [ ] ✅ Max drawdown acceptable

### System Ready:
- [ ] ✅ All technical checks passed
- [ ] ✅ Credentials verified
- [ ] ✅ Telegram working
- [ ] ✅ Angel One account ready

### Personal Readiness:
- [ ] ✅ Understand all settings
- [ ] ✅ Know the risks
- [ ] ✅ Have time to monitor Day 1
- [ ] ✅ Emergency plan ready
- [ ] ✅ Emotionally prepared for losses

---

## 🚦 FINAL DECISION

Count your ✅ checkmarks above:

- **All checkmarks complete?** → ✅ READY TO GO LIVE
- **Missing checkmarks?** → ⚠️ NOT READY - Complete pending items
- **Any concerns?** → ❌ DO NOT GO LIVE - More testing needed

---

## DAY 1 LIVE PLAN

### Morning Preparation (9:00 AM):
1. [ ] Open application: `./start_trader.sh`
2. [ ] Verify login successful
3. [ ] Check tokens refreshed (log will show)
4. [ ] Set mode to LIVE
5. [ ] Review settings one final time

### Start Trading (9:15 AM):
1. [ ] Click START button
2. [ ] Confirm "Real money risk" dialog
3. [ ] Watch log for first signal
4. [ ] Monitor Telegram continuously

### First Trade:
1. [ ] Note entry time: _______
2. [ ] Entry price: _______
3. [ ] Stop loss level: _______
4. [ ] Target level: _______
5. [ ] Verify order on Angel One app

### Mid-Day Check (12:00 PM):
1. [ ] Total trades so far: _______
2. [ ] Current P&L: Rs. _______
3. [ ] Any issues?: _______

### End of Day (3:30 PM):
1. [ ] Total trades: _______
2. [ ] Final P&L: Rs. _______
3. [ ] Win rate: _______%
4. [ ] Any errors?: _______
5. [ ] EOD report received on Telegram

### Day 1 Review:
- What went well: __________________________________________
- What needs adjustment: __________________________________________
- Continue live trading?: YES / NO / NEEDS ADJUSTMENT

---

## SIGNATURES (Optional but recommended)

I have completed this checklist and understand:
- This bot trades with REAL MONEY
- Losses are possible
- I have tested thoroughly in paper mode
- I will monitor closely on Day 1
- I know how to stop the bot in emergency
- I accept full responsibility for all trades

Name: _______________________
Date: _______________________
Signature: __________________

---

## 📞 IMPORTANT CONTACTS

- Angel One Customer Care: 1800 209 0909
- Angel One Trading Desk: _______________________
- Your Broker Contact: _______________________
- Technical Support: Check trader.log & GitHub issues

---

**Remember: Start Small → Monitor Closely → Scale Gradually**

**Good luck! May your trades be profitable! 📈**
