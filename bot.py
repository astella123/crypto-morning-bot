import json
import requests
import yfinance as yf

# 1. Legge il config
with open('config.json') as f:
    config = json.load(f)

# Token hardcoded per questo test (lo toglieremo dopo)
token = "8912873384:AAHPUXlXVxaMN1XBqO8cyz3ssdQL59sDGAo"
chat_id = config['telegram_chat_id']

# 2. Dati Crypto
portfolio = config['assets']['portfolio']
watchlist = config['assets']['watchlist']
tutte_le_crypto = portfolio + watchlist
crypto_ids = ",".join(tutte_le_crypto)

url_crypto = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_ids}&vs_currencies=usd&include_24hr_change=true"
dati_crypto = requests.get(url_crypto).json()

# 3. Dati Macro
sp500 = yf.Ticker(config['macro_indicators']['sp500']).info
dxy = yf.Ticker(config['macro_indicators']['dxy']).info

# 4. Dati Sentiment
url_fng = "https://api.alternative.me/fng/?limit=1"
dati_fng = requests.get(url_fng).json()['data'][0]

# 5. Costruzione Messaggio
messaggio = " *Crypto Morning Briefing*\n\n"

messaggio += "💼 *Portfolio*\n"
for crypto in portfolio:
    prezzo = dati_crypto[crypto]['usd']
    change = dati_crypto[crypto]['usd_24h_change']
    segno = "+" if change >= 0 else ""
    messaggio += f"  • {crypto.capitalize()}: ${prezzo:,.2f} ({segno}{change:.2f}%)\n"

messaggio += "\n👀 *Watchlist*\n"
for crypto in watchlist:
    prezzo = dati_crypto[crypto]['usd']
    change = dati_crypto[crypto]['usd_24h_change']
    segno = "+" if change >= 0 else ""
    messaggio += f"  • {crypto.capitalize()}: ${prezzo:,.2f} ({segno}{change:.2f}%)\n"

messaggio += "\n🌍 *Macro Indicators*\n"
messaggio += f"  • S&P 500: {sp500.get('regularMarketPrice', 'N/A'):,.2f}\n"
messaggio += f"  • DXY: {dxy.get('regularMarketPrice', 'N/A'):,.2f}\n"

messaggio += "\n *Market Sentiment*\n"
messaggio += f"  • Fear & Greed Index: **{dati_fng['value']}** ({dati_fng['value_classification']})\n"

# 6. Invio
payload = {"chat_id": chat_id, "text": messaggio, "parse_mode": "Markdown"}
url_telegram = f"https://api.telegram.org/bot{token}/sendMessage"
risposta = requests.post(url_telegram, json=payload)

print("Stato HTTP:", risposta.status_code)
print("Risposta API:", risposta.text)
