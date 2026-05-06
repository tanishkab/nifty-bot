# 🚀 DEPLOYMENT GUIDE - Nifty Auto Trader Web App

## Local Testing

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app_streamlit.py
```

3. Open browser at `http://localhost:8501`

---

## ☁️ Deploy to Streamlit Cloud (FREE)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Add Streamlit web app"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `nifty-options-bot`
5. Main file path: `app_streamlit.py`
6. Click "Deploy"

✅ Your app will be live at: `https://yourapp.streamlit.app`

**Note:** Free tier limits - app goes to sleep after inactivity. For 24/7 trading, use paid hosting below.

---

## 🖥️ Deploy to VPS (24/7 Trading)

### Option A: DigitalOcean / AWS EC2

1. Create Ubuntu VPS (Droplet/EC2)
2. SSH into server
3. Clone repo:
```bash
git clone https://github.com/yourusername/nifty-options-bot.git
cd nifty-options-bot
```

4. Install Python & dependencies:
```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```

5. Run with PM2 (process manager):
```bash
sudo apt install npm
sudo npm install -g pm2
pm2 start "streamlit run app_streamlit.py --server.port 8501" --name trader
pm2 save
pm2 startup
```

6. Setup nginx reverse proxy (optional):
```bash
sudo apt install nginx
sudo nano /etc/nginx/sites-available/trader
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/trader /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. Add SSL (free):
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🐳 Deploy with Docker

1. Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. Build & run:
```bash
docker build -t nifty-trader .
docker run -p 8501:8501 nifty-trader
```

3. Deploy to cloud:
   - **Railway.app** - Push to GitHub, connect repo, auto-deploy
   - **Render.com** - Connect GitHub, select Docker
   - **Fly.io** - `flyctl launch`

---

## 🔒 Security Best Practices

1. **Never commit credentials** - Use environment variables:
```python
import os
API_KEY = os.getenv("API_KEY")
```

2. Add `.env` file (gitignored):
```
API_KEY=your_key
CLIENT_ID=your_id
PASSWORD=your_password
TOTP=your_totp_secret
```

3. Load with:
```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
load_dotenv()
```

4. On Streamlit Cloud, add secrets in Settings → Secrets

---

## 📱 Access from Mobile

Once deployed, access your trading bot from anywhere:
- **Web Browser:** `https://your-app-url.com`
- **Mobile App:** Use Telegram bot for alerts

---

## ⚡ Performance Tips

1. **Use Redis for session state** (for multiple users)
2. **Enable caching** with `@st.cache_data`
3. **Use WebSocket** for real-time updates
4. **Run backtest as background job** (Celery/RQ)

---

## 💰 Cost Comparison

| Platform | Cost | Uptime | Speed |
|----------|------|--------|-------|
| Streamlit Cloud (Free) | $0 | Sleep after idle | Medium |
| Streamlit Cloud (Paid) | $20/mo | 24/7 | Fast |
| DigitalOcean Droplet | $6-12/mo | 24/7 | Fast |
| AWS EC2 t2.micro | ~$8/mo | 24/7 | Medium |
| Railway | $5/mo | 24/7 | Fast |

---

## 🆘 Troubleshooting

**App won't start:**
```bash
streamlit cache clear
pip install --upgrade streamlit
```

**SSL errors:**
- Already handled in code (verify=False)

**Port already in use:**
```bash
streamlit run app_streamlit.py --server.port 8502
```

---

## 📞 Support

Issues? Create GitHub issue or check `trader.log`
