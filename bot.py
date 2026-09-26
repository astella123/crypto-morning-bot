import json
import os
import requests
import yfinance as yf
import time

# --- 1. CONFIGURAZIONE E SECRETS ---
with open('config.json') as f:
    config = json.load(f)

token = os.environ.get('TELEGRAM_TOKEN')
gnews_key = os.environ.get('GNEWS_API_KEY')
chat_id = config['telegram_chat_id']

# Funzione per formattare i numeri in stile Europeo (€1.234,56)
def fmt_eur(val):
    if val is None: return "N/D"
    return f"€{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_pct(val):
    if val is None: return "N/D"
    segno = "+" if val >= 0 else ""
    return f"{segno}{val:.2f}%"

# --- 2. RACCOLTA DATI (Con paraurti try-except) ---
messaggio = "📊 *CRYPTO MORNING BRIEFING*\n\n"

# A. Portfolio Demo
messaggio += "💼 *PORTFOLIO DEMO*\n"
try:
    portfolio = config['assets']['portfolio_demo']
    ids = ",".join(portfolio.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=eur&include_24hr_change=true&include_7d_change=true" # Nota: 7d change richiede un endpoint diverso, usiamo markets sotto
    # Per avere 24h e 7d insieme usiamo /coins/markets per le crypto del portfolio
    url_markets = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&ids={ids}&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=24h,7d"
    dati_port = requests.get(url_markets).json()
    
    totale = 0
    for coin_id, qty in portfolio.items():
        coin_data = next((c for c in dati_port if c['id'] == coin_id), None)
        if coin_data:
            prezzo = coin_data['current_price']
            val_totale = prezzo * qty
            totale += val_totale
            c24 = coin_data.get('price_change_percentage_24h', 0)
            c7d = coin_data.get('price_change_percentage_7d_in_currency', 0)
            messaggio += f"• *{coin_id.capitalize()}* ({qty} {coin_id[:3].upper()})\n"
            messaggio += f"  1 unità: {fmt_eur(prezzo)} | Tuo: {fmt_eur(val_totale)}\n"
            messaggio += f"  📉 {fmt_pct(c24)} (24h) | 📈 {fmt_pct(c7d)} (7d)\n\n"
    messaggio += f"💰 *Totale Demo: {fmt_eur(totale)}*\n\n"
except Exception as e:
    messaggio += "⚠️ Errore caricamento Portfolio\n\n"

time.sleep(1.5) # Pausa per non superare i limiti API gratuiti

# B. Trending
messaggio += "🔥 *TRENDING (Hype)*\n"
try:
    url_trend = "https://api.coingecko.com/api/v3/search/trending"
    trend_data = requests.get(url_trend).json()['coins']
    for item in trend_data[:3]:
        c = item['item']
        prezzo = c.get('data', {}).get('price', 0)
        messaggio += f"• *{c['name']}*: {fmt_eur(prezzo)}\n"
except:
    messaggio += "N/D\n"

time.sleep(1.5)

# C. Top Gainers (7 giorni)
messaggio += "\n *TOP GAINERS (7d)*\n"
try:
    url_gainers = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&order=percent_change_7d_desc&per_page=3&page=1&sparkline=false&price_change_percentage=7d"
    gainers = requests.get(url_gainers).json()
    for g in gainers[:3]:
        c7d = g.get('price_change_percentage_7d_in_currency', 0)
        messaggio += f"• *{g['name']}*: {fmt_pct(c7d)}\n"
except:
    messaggio += "N/D\n"

# D. Macro & Sentiment (Logica Trend Follower)
messaggio += "\n🌍 *MACRO & CONTESTO*\n"
try:
    sp = yf.Ticker("^GSPC").info
    sp_prev = sp.get('regularMarketPreviousClose', 0)
    sp_curr = sp.get('regularMarketPrice', 0)
    sp_change = sp_curr - sp_prev if sp_curr and sp_prev else 0
    sp_emoji = "🟢" if sp_change >= 0 else "🔴"
    sp_msg = "Conviene Crypto" if sp_change >= 0 else "Attenzione"
    messaggio += f"• *S&P 500*: {sp_curr:,.0f} {sp_emoji} ({sp_msg})\n"
except:
    messaggio += "• S&P 500: N/D\n"

try:
    dxy = yf.Ticker("DX-Y.NYB").info
    dxy_prev = dxy.get('regularMarketPreviousClose', 0)
    dxy_curr = dxy.get('regularMarketPrice', 0)
    dxy_change = dxy_curr - dxy_prev if dxy_curr and dxy_prev else 0
    # Dollaro forte (su) = male per crypto, Dollaro debole (giu) = bene
    dxy_emoji = "🔴" if dxy_change >= 0 else "🟢"
    dxy_msg = "Attenzione" if dxy_change >= 0 else "Conviene Crypto"
    messaggio += f"• *DXY*: {dxy_curr:.2f} {dxy_emoji} ({dxy_msg})\n"
except:
    messaggio += "• DXY: N/D\n"

messaggio += "\n🧠 *MARKET SENTIMENT*\n"
try:
    fng = requests.get("https://api.alternative.me/fng/?limit=1").json()['data'][0]
    val = int(fng['value'])
    # Logica Trend Follower: >50 Avidità (Verde), <50 Paura (Rosso)
    fng_emoji = "🟢" if val >= 50 else "🔴"
    messaggio += f"• *Fear & Greed*: {val} ({fng['value_classification']}) {fng_emoji}\n"
except:
    messaggio += "• Fear & Greed: N/D\n"

# E. Notizie GNews
messaggio += "\n📰 *ULTIME NOTIZIE*\n"
if gnews_key:
    try:
        q = config['news']['query']
        url_news = f"https://gnews.io/api/v4/search?q={q}&lang={config['news']['lang']}&country={config['news']['country']}&max={config['news']['max_articles']}&apikey={gnews_key}"
        news = requests.get(url_news).json()['articles']
        for n in news[:3]:
            messaggio += f"• [{n['title']}]({n['url']})\n"
    except:
        messaggio += "N/D\n"
else:
    messaggio += "⚠️ Chiave GNews mancante nei Secrets\n"

# F. Legenda
messaggio += "\n━━━━━━━━━━━━━━━━━━━━\n"
messaggio += "📖 *GUIDA RAPIDA*\n"
messaggio += "🟢 = *Conviene* (Segnale positivo)\n"
messaggio += "🔴 = *Attenzione* (Segnale negativo)\n"
messaggio += "• *24h/7d*: Variazione ultime 24 ore / 7 giorni\n"
messaggio += "• *DXY*: Forza dollaro (se scende, crypto salgono)\n"
messaggio += "• *Fonti*: CoinGecko, Yahoo Finance, GNews"

# --- 3. INVIO ---
payload = {"chat_id": chat_id, "text": messaggio, "parse_mode": "Markdown"}
url_telegram = f"https://api.telegram.org/bot{token}/sendMessage"
risposta = requests.post(url_telegram, json=payload)

print("Stato HTTP:", risposta.status_code)
print("Risposta API:", risposta.text)
