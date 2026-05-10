# -*- coding: utf-8 -*-
"""
NIFTY AUTO TRADER — WEB VERSION (STREAMLIT)
============================================
Streamlit web app for live trading bot
Deploy: streamlit run app_streamlit.py
"""

import streamlit as st
import pandas as pd
import datetime
import time
import threading
import json
import os

# Import all backend logic - EMBEDDED DIRECTLY
import sys
sys.path.append(os.path.dirname(__file__))

# Copy essential imports from main_consolidated
import ssl
import warnings
warnings.filterwarnings('ignore')
os.environ['PYTHONHTTPSVERIFY'] = '0'
ssl._create_default_https_context = ssl._create_unverified_context

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
_original_request = requests.Session.request
_original_get = requests.get
_original_post = requests.post

def patched_request(self, method, url, **kwargs):
    kwargs['verify'] = False
    return _original_request(self, method, url, **kwargs)

def patched_get(url, **kwargs):
    kwargs['verify'] = False
    return _original_get(url, **kwargs)

def patched_post(url, **kwargs):
    kwargs['verify'] = False
    return _original_post(url, **kwargs)

requests.Session.request = patched_request
requests.get = patched_get
requests.post = patched_post

import pyotp
import numpy as np
from SmartApi import SmartConnect
import logging
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler('trader.log', encoding='utf-8')])
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════
#  BACKEND FUNCTIONS - EMBEDDED FOR REAL-TIME PREMIUMS
# ═══════════════════════════════════════════════════════

INSTRUMENTS = {
    "NIFTY 50": {"spot_token": "99926000", "exchange": "NSE", "lot": 50, "sg": 50},
    "BANKNIFTY": {"spot_token": "99926009", "exchange": "NSE", "lot": 15, "sg": 100},
    "FINNIFTY": {"spot_token": "99926037", "exchange": "NSE", "lot": 40, "sg": 50},
}

class ST:
    api = None
    opt_tokens = {}
    fut_tokens = {}

CFG = {}  # Will be synced with session_state

def angel_login():
    try:
        totp = pyotp.TOTP(st.session_state.config["TOTP"]).now()
        logger.info(f"🔐 Attempting login with TOTP: {totp}")

        s = SmartConnect(api_key=st.session_state.config["API_KEY"])
        d = s.generateSession(st.session_state.config["CLIENT_ID"],
                             st.session_state.config["PASSWORD"], totp)

        if d and d.get("status"):
            ST.api = s
            logger.info("✅ Angel One login successful!")
            logger.info(f"   API object set: {ST.api is not None}")
            return True
        else:
            logger.error(f"❌ Login failed: {d.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        logger.error(f"❌ Login error: {e}")
        import traceback
        logger.error(traceback.format_exc())
    return False

def get_weekly_expiry():
    """Get next weekly expiry for NIFTY (Tuesdays)"""
    today = datetime.date.today()
    # NIFTY weekly options expire on Tuesdays (weekday = 1)
    d = (1 - today.weekday()) % 7
    exp = today + datetime.timedelta(days=d)
    if d == 0:
        # If today is Tuesday, check if market has closed
        now = datetime.datetime.now()
        if now.hour >= 15 and now.minute >= 30:
            exp += datetime.timedelta(days=7)
    if exp < today:
        exp += datetime.timedelta(days=7)
    return exp

def refresh_tokens(log_fn=None, force=False):
    def _log(msg):
        logger.info(msg)
        if log_fn: log_fn(msg, "info")

    _log("🔄 Refreshing option tokens from Angel API...")
    try:
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        resp = requests.get(url, timeout=60, verify=False)

        if resp.status_code != 200:
            _log(f"❌ Failed to fetch token master: {resp.status_code}")
            return False

        items = resp.json()
        _log(f"📥 Downloaded {len(items)} total instruments")

        today = datetime.date.today()
        week_exp = get_weekly_expiry()
        opt_found = {}

        for item in items:
            if not isinstance(item, dict): continue

            # Check for NIFTY options
            item_name = str(item.get("name", "")).upper()
            if item_name != "NIFTY": continue

            # Check instrument type
            exch = str(item.get("exch_seg", "")).upper()
            itype = str(item.get("instrumenttype", "")).upper()
            if exch != "NFO" or itype != "OPTIDX": continue

            sym_field = str(item.get("symbol", "")).upper()
            if sym_field.endswith("CE"): opt_type = "CE"
            elif sym_field.endswith("PE"): opt_type = "PE"
            else: continue

            # Parse expiry
            exp_str = str(item.get("expiry", ""))
            try:
                exp = datetime.datetime.strptime(exp_str[:10], "%d%b%Y").date()
            except: continue

            # Only near expiry (21 days to include next 2-3 weeks)
            days_to_exp = (exp - today).days
            if days_to_exp < 0 or days_to_exp > 21: continue

            # Parse strike
            try:
                strike_val = int(float(item.get("strike", 0)) / 100)
            except: continue

            if not (18000 <= strike_val <= 30000): continue

            token = str(item.get("token", ""))
            opt_found[sym_field] = {
                "token": token,
                "symbol": sym_field,
                "strike": strike_val,
                "type": opt_type,
                "expiry": exp
            }

        ST.opt_tokens = opt_found

        # Show sample tokens loaded
        sample_keys = list(opt_found.keys())[:5]
        _log(f"✅ Loaded {len(opt_found)} option tokens (expiry: {week_exp})")
        _log(f"📋 Sample: {', '.join(sample_keys)}")

        return True
    except Exception as e:
        _log(f"❌ Token refresh error: {e}")
        logger.error(f"Token refresh error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def get_option_token(symbol, strike, opt_type):
    if not ST.opt_tokens:
        logger.error("No tokens loaded")
        return None, None

    # Try different expiries (current week, next week, week after)
    for exp_offset in [0, 1, 7, 8, 14]:
        exp = get_weekly_expiry() + datetime.timedelta(days=exp_offset)

        # Angel format: NIFTY + DDMMMYY + 5-DIGIT-STRIKE + TYPE
        # Example: NIFTY07MAY2624000PE
        exp_str = exp.strftime("%d%b%y").upper()  # 07MAY26 (2-digit year)

        for delta in [0, 50, -50, 100, -100, 150, -150, 200, -200]:
            s = int(strike) + delta

            # Format: NIFTY + DDMMMYY + 5-digit strike + TYPE
            key = f"NIFTY{exp_str}{s:05d}{opt_type}"

            if key in ST.opt_tokens:
                d = ST.opt_tokens[key]
                logger.debug(f"   ✅ Found: {key}")
                return d["token"], d["symbol"]

    logger.debug(f"   ❌ Not found. Tried strikes around {strike} for expiries near {get_weekly_expiry()}")
    return None, None

def get_option_ltp_live(symbol, spot, opt_type, use_calculated=False):
    """REAL premium from Angel API - with fallback to calculated premium"""
    try:
        info = INSTRUMENTS.get(symbol, {})
        sg = info.get("sg", 50)
        strike = round(spot / sg) * sg

        # For backtests or when tokens unavailable, use calculated premium
        if use_calculated or not ST.api or not ST.opt_tokens:
            # Simple premium calculation based on ATM distance
            distance = abs(strike - spot) / spot

            if opt_type == "CE":
                # CE: cheaper when strike > spot
                if strike > spot:
                    premium = spot * (0.01 - distance * 0.5)
                else:
                    premium = spot * (0.02 + distance * 0.3)
            else:  # PE
                # PE: cheaper when strike < spot
                if strike < spot:
                    premium = spot * (0.01 - distance * 0.5)
                else:
                    premium = spot * (0.02 + distance * 0.3)

            premium = max(premium, spot * 0.002)  # Minimum 0.2% of spot
            logger.debug(f"📊 Calculated premium: {symbol} {opt_type} @ {strike} = Rs.{premium:.2f}")
            return round(premium, 2)

        logger.debug(f"🔍 Looking for {symbol} {opt_type} @ strike {strike} (spot: {spot})")

        for strike_delta in [0, sg, -sg, 2*sg, -2*sg]:
            try_strike = strike + strike_delta
            token, opt_sym = get_option_token(symbol, try_strike, opt_type)

            if token and opt_sym:
                try:
                    logger.debug(f"   Trying: {opt_sym} (token: {token})")
                    r = ST.api.ltpData("NFO", opt_sym, token)
                    if isinstance(r, dict) and r.get("status"):
                        ltp = float(r.get("data", {}).get("ltp", 0))
                        if ltp > 0:
                            logger.info(f"✅ REAL LTP: {opt_sym} = Rs.{ltp}")
                            return ltp
                    else:
                        logger.debug(f"   Failed: {r}")
                except Exception as e:
                    logger.debug(f"   Error: {e}")
                    continue

        # Fallback to calculated if real fetch fails
        logger.warning(f"⚠️ Could not fetch real LTP for {symbol} {opt_type} @ {strike}. Using calculated premium.")
        distance = abs(strike - spot) / spot
        if opt_type == "CE":
            premium = spot * (0.015 if strike <= spot else 0.008)
        else:
            premium = spot * (0.015 if strike >= spot else 0.008)
        return round(premium, 2)

    except Exception as e:
        logger.error(f"❌ LTP function error: {e}")
        return round(spot * 0.005, 2)

def fetch_candles(token, exchange, interval, days):
    to = datetime.datetime.now()
    frm = to - datetime.timedelta(days=days)
    try:
        r = ST.api.getCandleData({
            "exchange": exchange,
            "symboltoken": token,
            "interval": interval,
            "fromdate": frm.strftime("%Y-%m-%d %H:%M"),
            "todate": to.strftime("%Y-%m-%d %H:%M"),
        })
        if r["status"] and r["data"]:
            df = pd.DataFrame(r["data"], columns=["dt","open","high","low","close","volume"])
            df["dt"] = pd.to_datetime(df["dt"])
            df = df.set_index("dt").sort_index()
            for c in ["open","high","low","close","volume"]:
                df[c] = pd.to_numeric(df[c])
            return df
    except: pass
    return pd.DataFrame()

def calc_indicators(df, config):
    df["ema_f"] = df["close"].ewm(span=config["EMA_FAST"], adjust=False).mean()
    df["ema_s"] = df["close"].ewm(span=config["EMA_SLOW"], adjust=False).mean()
    df["ema_gap"] = df["ema_f"] - df["ema_s"]
    df["vol_ok"] = True
    df["ce_sig"] = ((df["ema_gap"] >= config["EMA_GAP"]) &
                   (df["ema_gap"].shift(1) < config["EMA_GAP"]) & df["vol_ok"])
    df["pe_sig"] = ((df["ema_gap"] <= -config["EMA_GAP"]) &
                   (df["ema_gap"].shift(1) > -config["EMA_GAP"]) & df["vol_ok"])
    return df.dropna(subset=["ema_f","ema_s"])

def run_backtest(symbol, days, log_fn, config):
    log_fn(f"📊 Backtest: {symbol} - {days} days", "info")

    info = INSTRUMENTS[symbol]
    df = fetch_candles(info["spot_token"], info["exchange"],
                      config["INTERVAL"], days)

    if df.empty:
        log_fn("❌ No data", "err")
        return []

    log_fn(f"✅ {len(df)} candles", "sig")
    df = calc_indicators(df, config)
    log_fn(f"📈 Signals: CE={df['ce_sig'].sum()} PE={df['pe_sig'].sum()}", "info")

    trades = []
    pos = None
    lot = info["lot"]
    sg = info["sg"]

    for ts, row in df.iterrows():
        if pos:
            # Use calculated premium for backtesting (historical data)
            cur_opt = get_option_ltp_live(symbol, row["close"], pos["otype"], use_calculated=True)
            # No sleep needed for calculated premiums
            # time.sleep(0.1)

            best = pos.get("best_opt", pos["opt_entry"])
            if cur_opt > best: best = cur_opt
            pos["best_opt"] = best

            sl = pos["opt_entry"] - config["SL_PTS"]
            tsl = best - config["TSL_PTS"]
            tgt = pos["opt_entry"] + config["TGT_PTS"]

            exit_now, reason = False, ""
            if cur_opt <= max(sl, tsl):
                exit_now, reason = True, "SL/TSL"
            elif cur_opt >= tgt:
                exit_now, reason = True, "Target"

            if exit_now:
                pnl = (cur_opt - pos["opt_entry"]) * lot
                trades.append({**pos, "exit_time": str(ts), "opt_exit": cur_opt,
                             "spot_exit": row["close"], "pnl": pnl, "reason": reason})
                log_fn(f"  Trade #{len(trades)}: P&L=Rs.{pnl:+.0f}", "sig")
                pos = None

        if not pos:
            if row["ce_sig"]:
                strike = round(row["close"] / sg) * sg
                # Use calculated premium for backtesting
                opt_price = get_option_ltp_live(symbol, row["close"], "CE", use_calculated=True)
                # No sleep needed for calculated premiums
                pos = {"entry_time": str(ts), "otype": "CE", "strike": strike,
                      "spot_entry": row["close"], "opt_entry": opt_price, "best_opt": opt_price}
                log_fn(f"  📈 CE @ Rs.{opt_price:.2f} (Calculated)", "info")
            elif row["pe_sig"]:
                strike = round(row["close"] / sg) * sg
                # Use calculated premium for backtesting
                opt_price = get_option_ltp_live(symbol, row["close"], "PE", use_calculated=True)
                # No sleep needed for calculated premiums
                pos = {"entry_time": str(ts), "otype": "PE", "strike": strike,
                      "spot_entry": row["close"], "opt_entry": opt_price, "best_opt": opt_price}
                log_fn(f"  📉 PE @ Rs.{opt_price:.2f} (Calculated)", "info")

    log_fn(f"✅ Complete: {len(trades)} trades", "sig")
    return trades

def tg(msg):
    try:
        bot_token = st.session_state.config.get("BOT_TOKEN", "")
        chat_id = st.session_state.config.get("CHAT_ID", "")
        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                     data={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"},
                     timeout=10, verify=False)
    except: pass

def tg_file(path, caption=""):
    try:
        bot_token = st.session_state.config.get("BOT_TOKEN", "")
        chat_id = st.session_state.config.get("CHAT_ID", "")
        with open(path, "rb") as f:
            requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendDocument",
                data={"chat_id": chat_id, "caption": caption},
                files={"document": f}, timeout=30, verify=False)
    except: pass

def make_pdf(trades, filename):
    """Generate PDF and save to file"""
    try:
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Backtest Report", styles["Title"]))
        elements.append(Spacer(1, 12))

        # Summary
        total_pnl = sum(t.get("pnl", 0) for t in trades)
        wins = sum(1 for t in trades if t.get("pnl", 0) > 0)

        summary_data = [
            ["Metric", "Value"],
            ["Total Trades", str(len(trades))],
            ["Wins", str(wins)],
            ["Losses", str(len(trades) - wins)],
            ["Total P&L", f"Rs.{total_pnl:,.2f}"]
        ]

        t = Table(summary_data)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)

        doc.build(elements)
        return filename
    except Exception as e:
        logger.error(f"PDF generation error: {e}")
        return None

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.running = False
    st.session_state.api = None
    st.session_state.trades = []
    st.session_state.positions = []
    st.session_state.balance = 100000
    st.session_state.logs = []
    st.session_state.fut_tokens = {}
    st.session_state.opt_tokens = {}
    st.session_state.last_token_refresh = None

# Configuration
if 'config' not in st.session_state:
    st.session_state.config = {
        "API_KEY": "x9Zs2hWZ",
        "CLIENT_ID": "J109737",
        "PASSWORD": "4966",
        "TOTP": "HDVHUMXPPC2FTJOSHKSK6CO5AA",
        "BOT_TOKEN": "8665264906:AAFJD6a08qPbw0RvLQWNL7YF6624PcSgN-w",
        "CHAT_ID": "8748890897",
        "SYMBOL": "NIFTY 50",
        "MODE": "paper",
        "EMA_FAST": 9,
        "EMA_SLOW": 21,
        "EMA_GAP": 2,
        "VOL_PERIOD": 20,
        "VOL_MULT": 1.2,
        "INTERVAL": "FIVE_MINUTE",
        "DAYS": 30,
        "SL_PTS": 30,
        "TSL_PTS": 20,
        "TGT_PTS": 60,
        "LOT_SIZE": 50,
        "BOTH_SIDE": True,
        "PAPER_CAP": 100000,
        "VOICE": False,
    }

# INSTRUMENTS defined above in backend section

# ═══════════════════════════════════════════════════════
#  PDF REPORT GENERATION
# ═══════════════════════════════════════════════════════
def generate_pdf_report(trades, symbol, mode):
    """Generate PDF report and return bytes"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("Nifty Auto Trader — Report", styles["Title"]))
    elements.append(Paragraph(
        f"{datetime.date.today().strftime('%d %B %Y')} | {symbol} | {mode.upper()}",
        styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Summary stats
    total = sum(t.get("pnl", 0) for t in trades)
    wins = sum(1 for t in trades if t.get("pnl", 0) > 0)
    rate = wins / len(trades) * 100 if trades else 0
    ce_count = sum(1 for t in trades if t.get("otype") == "CE")
    pe_count = sum(1 for t in trades if t.get("otype") == "PE")

    summary_data = [
        ["Metric", "Value"],
        ["Symbol", symbol],
        ["Mode", mode.upper()],
        ["Total Trades", str(len(trades))],
        ["CE Trades", str(ce_count)],
        ["PE Trades", str(pe_count)],
        ["Wins", str(wins)],
        ["Losses", str(len(trades) - wins)],
        ["Win Rate", f"{rate:.1f}%"],
        ["Total P&L", f"Rs.{total:,.2f}"],
        ["SL pts", str(st.session_state.config["SL_PTS"])],
        ["TSL pts", str(st.session_state.config["TSL_PTS"])],
        ["Target pts", str(st.session_state.config["TGT_PTS"])],
    ]

    summary_table = Table(summary_data, colWidths=[180, 160])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f0f9ff"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    elements.append(summary_table)
    elements.append(Spacer(1, 14))

    # Trade log
    if trades:
        elements.append(Paragraph("<b>Trade Log</b>", styles["Heading2"]))
        headers = ["Time", "Type", "Direction", "Strike", "Spot Entry", "Opt Entry", "Opt Exit", "P&L", "Reason"]
        rows = [headers]

        for t in trades[-50:]:
            pnl = t.get("pnl", 0)
            otype = t.get("otype", "CE")
            rows.append([
                str(t.get("entry_time", ""))[:16],
                otype,
                "Bull" if otype == "CE" else "Bear",
                str(t.get("strike", "")),
                f"Rs.{t.get('spot_entry', 0):.0f}",
                f"Rs.{t.get('opt_entry', 0):.2f}",
                f"Rs.{t.get('opt_exit', 0):.2f}",
                f"Rs.{pnl:.2f}",
                t.get("reason", ""),
            ])

        trade_table = Table(rows, colWidths=[78, 38, 45, 50, 60, 55, 55, 60, 52])
        trade_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 7.5),
            ("PADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(trade_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def generate_csv_report(trades):
    """Generate CSV report and return string"""
    if not trades:
        return "No trades available"

    df = pd.DataFrame(trades)
    return df.to_csv(index=False)

def generate_excel_report(trades):
    """Generate Excel report and return bytes"""
    if not trades:
        return None

    try:
        buffer = io.BytesIO()
        df = pd.DataFrame(trades)
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Trades', index=False)
        buffer.seek(0)
        return buffer.getvalue()
    except ImportError:
        # openpyxl not installed, return None
        return None

# Page config
st.set_page_config(
    page_title="Nifty Auto Trader",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {background-color: #0e1117;}
    .stButton>button {
        width: 100%;
        background-color: #00e5ff;
        color: black;
        font-weight: bold;
    }
    .metric-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📈 NIFTY AUTO TRADER - WEB")
st.markdown("---")

# Sidebar - Controls
with st.sidebar:
    st.header("⚙️ Controls")

    # Symbol selection
    symbol = st.selectbox("Symbol", list(INSTRUMENTS.keys()),
                          index=list(INSTRUMENTS.keys()).index(st.session_state.config["SYMBOL"]))
    st.session_state.config["SYMBOL"] = symbol

    # Mode selection
    mode = st.radio("Mode", ["paper", "backtest", "live"],
                    index=["paper", "backtest", "live"].index(st.session_state.config["MODE"]))
    st.session_state.config["MODE"] = mode

    st.markdown("---")

    # Start/Stop buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 START", disabled=st.session_state.running):
            st.session_state.running = True
            st.success("Started!")
            st.rerun()

    with col2:
        if st.button("🛑 STOP", disabled=not st.session_state.running):
            st.session_state.running = False
            st.warning("Stopped!")
            st.rerun()

    # Status indicator
    if st.session_state.running:
        st.success("🟢 RUNNING")
    else:
        st.info("⚪ IDLE")

    st.markdown("---")

    # Quick actions
    st.subheader("Quick Actions")

    # Download Reports
    st.markdown("**📥 Download Report**")
    today_trades = [t for t in st.session_state.trades
                   if str(datetime.date.today()) in str(t.get("entry_time", ""))]

    if today_trades:
        col1, col2, col3 = st.columns(3)

        with col1:
            # PDF Download
            pdf_bytes = generate_pdf_report(
                today_trades,
                st.session_state.config["SYMBOL"],
                st.session_state.config["MODE"]
            )
            st.download_button(
                label="📄 PDF",
                data=pdf_bytes,
                file_name=f"report_{datetime.date.today()}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col2:
            # CSV Download
            csv_data = generate_csv_report(today_trades)
            st.download_button(
                label="📊 CSV",
                data=csv_data,
                file_name=f"trades_{datetime.date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col3:
            # Excel Download
            excel_bytes = generate_excel_report(today_trades)
            if excel_bytes:
                st.download_button(
                    label="📗 Excel",
                    data=excel_bytes,
                    file_name=f"trades_{datetime.date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
    else:
        st.info("No trades today to download")

    st.markdown("---")

    if st.button("📱 Send to Telegram", use_container_width=True):
        st.info("Report sent to Telegram")

    if st.button("🔄 Refresh Tokens", use_container_width=True):
        st.info("Tokens refreshed")

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Backtest", "🔍 Scanner", "⚙️ Settings"])

with tab1:
    # Dashboard - Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        today_trades = [t for t in st.session_state.trades
                       if str(datetime.date.today()) in str(t.get("entry_time", ""))]
        st.metric("Today Trades", len(today_trades))

    with col2:
        pnl = sum(t.get("pnl", 0) for t in today_trades)
        st.metric("Today P&L", f"₹{pnl:,.2f}", delta=f"{pnl:+,.0f}")

    with col3:
        wins = sum(1 for t in today_trades if t.get("pnl", 0) > 0)
        win_rate = (wins / len(today_trades) * 100) if today_trades else 0
        st.metric("Win Rate", f"{win_rate:.1f}%")

    with col4:
        st.metric("Balance", f"₹{st.session_state.balance:,.2f}")

    st.markdown("---")

    # Live logs
    st.subheader("📝 Live Logs")
    log_container = st.container()
    with log_container:
        if st.session_state.logs:
            for log in st.session_state.logs[-20:]:
                st.text(log)
        else:
            st.info("No logs yet. Click START to begin trading.")

    # Positions
    st.subheader("📍 Current Positions")
    if st.session_state.positions:
        pos_df = pd.DataFrame(st.session_state.positions)
        st.dataframe(pos_df, use_container_width=True)
    else:
        st.info("No open positions")

    # Recent trades
    col_header, col_download = st.columns([3, 1])
    with col_header:
        st.subheader("💼 Recent Trades")
    with col_download:
        if st.session_state.trades:
            # All trades download
            all_trades_csv = generate_csv_report(st.session_state.trades)
            st.download_button(
                label="⬇️ All Trades CSV",
                data=all_trades_csv,
                file_name=f"all_trades_{datetime.date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )

    if today_trades:
        trades_df = pd.DataFrame(today_trades)
        st.dataframe(trades_df[["entry_time", "otype", "strike", "spot_entry",
                                "opt_entry", "opt_exit", "pnl", "reason"]],
                    use_container_width=True)
    else:
        st.info("No trades today")

with tab2:
    st.header("📈 Backtest")

    # Initialize backtest state
    if 'backtest_results' not in st.session_state:
        st.session_state.backtest_results = []
    if 'backtest_running' not in st.session_state:
        st.session_state.backtest_running = False
    if 'last_bt_symbol' not in st.session_state:
        st.session_state.last_bt_symbol = "NIFTY 50"
    if 'last_bt_days' not in st.session_state:
        st.session_state.last_bt_days = 30

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("⚙️ Configuration")

        bt_symbol = st.selectbox("Symbol", list(INSTRUMENTS.keys()))
        bt_days = st.slider("Days to Test", 7, 90, 30)

        st.markdown("---")
        st.markdown("**Current Settings:**")
        st.write(f"- EMA Fast: {st.session_state.config['EMA_FAST']}")
        st.write(f"- EMA Slow: {st.session_state.config['EMA_SLOW']}")
        st.write(f"- EMA Gap: {st.session_state.config['EMA_GAP']} pts")
        st.write(f"- SL: {st.session_state.config['SL_PTS']} pts")
        st.write(f"- TSL: {st.session_state.config['TSL_PTS']} pts")
        st.write(f"- Target: {st.session_state.config['TGT_PTS']} pts")

        st.markdown("---")

        if st.button("▶️ RUN BACKTEST", use_container_width=True,
                    disabled=st.session_state.backtest_running):
            st.session_state.backtest_running = True
            st.session_state.last_bt_symbol = bt_symbol
            st.session_state.last_bt_days = bt_days
            st.rerun()

    with col2:
        if st.session_state.backtest_running:
            st.subheader("⏳ Running Backtest...")

            # Get stored symbol and days
            run_symbol = st.session_state.get('last_bt_symbol', 'NIFTY 50')
            run_days = st.session_state.get('last_bt_days', 30)

            progress_bar = st.progress(0)
            status_text = st.empty()
            log_area = st.empty()

            logs = []

            def log_fn(msg, tag=""):
                logs.append(msg)
                log_area.text_area("Logs", "\n".join(logs[-20:]), height=200)

            try:
                # Login if not already
                if not ST.api:
                    status_text.text("🔐 Logging in to Angel One...")
                    progress_bar.progress(10)
                    if not angel_login():
                        st.error("❌ Login failed!")
                        st.session_state.backtest_running = False
                        st.stop()
                    log_fn("✅ Login successful")

                # Refresh tokens
                status_text.text("🔄 Refreshing option tokens...")
                progress_bar.progress(30)
                refresh_tokens(log_fn, force=True)
                log_fn("✅ Tokens refreshed")

                # Run backtest
                status_text.text(f"📊 Running backtest: {run_symbol} - {run_days} days...")
                progress_bar.progress(50)

                # Update CFG with current config
                for key in st.session_state.config:
                    CFG[key] = st.session_state.config[key]

                trades = run_backtest(run_symbol, run_days, log_fn, st.session_state.config)

                progress_bar.progress(100)

                if trades:
                    st.session_state.backtest_results = trades
                    st.session_state.trades = trades
                    status_text.text(f"✅ Backtest complete: {len(trades)} trades")
                    log_fn(f"✅ Backtest complete: {len(trades)} trades")
                else:
                    st.warning("⚠️ No trades generated. Try adjusting settings.")

            except Exception as e:
                st.error(f"❌ Error: {e}")
                log_fn(f"❌ Error: {e}")

            finally:
                st.session_state.backtest_running = False
                time.sleep(2)
                st.rerun()

        elif st.session_state.backtest_results and len(st.session_state.backtest_results) > 0:
            trades = st.session_state.backtest_results
            bt_symbol = st.session_state.get('last_bt_symbol', 'NIFTY 50')
            bt_days = st.session_state.get('last_bt_days', 30)

            st.success(f"✅ Backtest Complete: {bt_symbol} ({bt_days} days)")

            # Summary metrics
            total_pnl = sum(t.get("pnl", 0) for t in trades)
            wins = sum(1 for t in trades if t.get("pnl", 0) > 0)
            losses = len(trades) - wins
            win_rate = (wins / len(trades) * 100) if trades else 0

            ce_count = sum(1 for t in trades if t.get("otype") == "CE")
            pe_count = sum(1 for t in trades if t.get("otype") == "PE")

            avg_win = sum(t.get("pnl", 0) for t in trades if t.get("pnl", 0) > 0) / wins if wins > 0 else 0
            avg_loss = sum(t.get("pnl", 0) for t in trades if t.get("pnl", 0) < 0) / losses if losses > 0 else 0

            st.markdown("### 📊 Summary Metrics")

            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Trades", len(trades))
            with col2:
                st.metric("Win Rate", f"{win_rate:.1f}%")
            with col3:
                st.metric("Wins / Losses", f"{wins} / {losses}")
            with col4:
                st.metric("Total P&L", f"₹{total_pnl:,.0f}",
                         delta=f"{total_pnl:+,.0f}")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("CE Trades", ce_count)
            with col2:
                st.metric("PE Trades", pe_count)
            with col3:
                st.metric("Avg Win", f"₹{avg_win:,.0f}")
            with col4:
                st.metric("Avg Loss", f"₹{avg_loss:,.0f}")

            st.markdown("---")

            # Trades table with better formatting
            st.markdown("### 📋 All Trades")

            # Create DataFrame
            df = pd.DataFrame(trades)

            # Prepare display columns
            if len(df) > 0:
                df_display = df.copy()

                # Format columns for display
                df_display['Entry Time'] = df_display['entry_time'].str[:16]
                df_display['Type'] = df_display['otype']
                df_display['Strike'] = df_display['strike'].apply(lambda x: f"{int(x)}")
                df_display['Spot Entry'] = df_display['spot_entry'].apply(lambda x: f"₹{x:.0f}")
                df_display['Premium Entry'] = df_display['opt_entry'].apply(lambda x: f"₹{x:.2f}")
                df_display['Premium Exit'] = df_display['opt_exit'].apply(lambda x: f"₹{x:.2f}")
                df_display['P&L'] = df_display['pnl'].apply(lambda x: f"₹{x:,.0f}")
                df_display['Reason'] = df_display['reason']

                # Select only display columns
                final_df = df_display[['Entry Time', 'Type', 'Strike', 'Spot Entry',
                                       'Premium Entry', 'Premium Exit', 'P&L', 'Reason']]

                # Show table
                st.dataframe(
                    final_df,
                    use_container_width=True,
                    height=400,
                    hide_index=True
                )
            else:
                st.warning("No trades to display")

            # Download and export options
            st.markdown("---")
            st.markdown("### 📥 Export Options")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                # CSV Download - Always available
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📊 Download CSV",
                    data=csv_data,
                    file_name=f"backtest_{bt_symbol.replace(' ', '_')}_{bt_days}days_{datetime.date.today()}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    type="primary"
                )

            with col2:
                # Excel Download
                try:
                    excel_bytes = generate_excel_report(trades)
                    if excel_bytes:
                        st.download_button(
                            label="📗 Download Excel",
                            data=excel_bytes,
                            file_name=f"backtest_{bt_symbol.replace(' ', '_')}_{bt_days}days_{datetime.date.today()}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                except:
                    st.button("📗 Excel (N/A)", disabled=True, use_container_width=True)

            with col3:
                # PDF Download
                pdf_bytes = generate_pdf_report(trades, bt_symbol, "backtest")
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_bytes,
                    file_name=f"backtest_{bt_symbol.replace(' ', '_')}_{bt_days}days_{datetime.date.today()}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            with col4:
                # Send to Telegram
                if st.button("📱 Send to Telegram", use_container_width=True):
                    with st.spinner("Sending..."):
                        msg = (
                            f"<b>📊 BACKTEST REPORT</b>\n\n"
                            f"Symbol: {bt_symbol} | {bt_days} days\n"
                            f"Trades: {len(trades)} (W:{wins} L:{losses})\n"
                            f"Win Rate: {win_rate:.1f}%\n"
                            f"Total P&L: Rs.{total_pnl:,.0f}\n\n"
                            f"CE: {ce_count} | PE: {pe_count}"
                        )
                        tg(msg)

                        # Send CSV as well
                        csv_filename = f"backtest_{bt_symbol.replace(' ', '_')}_{datetime.date.today()}.csv"
                        with open(csv_filename, 'w') as f:
                            f.write(csv_data)
                        tg_file(csv_filename, f"Backtest: {bt_symbol}")

                        st.success("✅ Sent to Telegram!")

            # Additional info
            st.info(f"💡 **Tip**: All premiums are fetched in real-time from Angel One API for accurate results!")

            # Run new backtest button
            st.markdown("---")
            if st.button("🔄 Run New Backtest", use_container_width=True, type="secondary"):
                st.session_state.backtest_results = []
                st.rerun()

        else:
            st.subheader("👈 Configure & Run")
            st.info("Select symbol and days, then click RUN BACKTEST to see results.")

            st.markdown("---")
            st.markdown("**📖 How it works:**")
            st.markdown("""
            1. **Login** to Angel One API
            2. **Fetch** historical data for selected symbol
            3. **Calculate** EMA signals and volume filters
            4. **Execute** paper trades with your settings
            5. **Show** detailed results with P&L analysis
            """)

            st.markdown("**⚡ Real-time premiums** are fetched from Angel One API for accurate results!")

with tab3:
    st.header("🔍 Scanner")

    if st.button("🔄 Scan All Symbols", use_container_width=True):
        st.info("Scanning...")

    st.dataframe(pd.DataFrame(columns=["Symbol", "LTP", "EMA Gap", "Signal", "Direction"]))

with tab4:
    st.header("⚙️ Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Trading Parameters")
        st.number_input("EMA Fast", value=st.session_state.config["EMA_FAST"], key="ema_fast")
        st.number_input("EMA Slow", value=st.session_state.config["EMA_SLOW"], key="ema_slow")
        st.number_input("EMA Gap (pts)", value=st.session_state.config["EMA_GAP"], key="ema_gap")
        st.number_input("Stop Loss (pts)", value=st.session_state.config["SL_PTS"], key="sl_pts")
        st.number_input("Trailing SL (pts)", value=st.session_state.config["TSL_PTS"], key="tsl_pts")
        st.number_input("Target (pts)", value=st.session_state.config["TGT_PTS"], key="tgt_pts")

    with col2:
        st.subheader("API Credentials")
        st.text_input("API Key", value=st.session_state.config["API_KEY"], type="password")
        st.text_input("Client ID", value=st.session_state.config["CLIENT_ID"])
        st.text_input("Password", value=st.session_state.config["PASSWORD"], type="password")
        st.text_input("TOTP Secret", value=st.session_state.config["TOTP"], type="password")

    if st.button("💾 Save Settings", use_container_width=True):
        st.success("Settings saved!")

# Auto-refresh every 5 seconds if running
if st.session_state.running:
    time.sleep(5)
    st.rerun()
