#  Crypto Morning Bot

Un bot automatizzato che invia ogni mattina un **Crypto Morning Briefing** professionale direttamente su Telegram. 

Progettato per fornire un quadro completo e immediato del mercato crypto e macroeconomico prima dell'apertura delle borse, trasformando dati grezzi in insight azionabili.

![Crypto Morning Briefing)

## ✨ Funzionalità Principali

Il bot genera un report giornaliero strutturato in 5 sezioni chiave:

- 💼 **Portfolio Demo**: Calcolo del valore attuale e delle variazioni (24h e 7d) di un portafoglio fittizio.
- 🔥 **Trending & Top Gainers**: Analisi dell'hype di mercato (ricerche CoinGecko) e delle crypto con le migliori performance settimanali.
- 🌍 **Macro & Contesto**: Monitoraggio di S&P 500 e DXY (Indice del Dollaro) con interpretazione automatica dell'impatto sulle crypto.
- 🧠 **Market Sentiment**: Indice Fear & Greed con logica Trend Follower.
- 📰 **Ultime Notizie**: Aggregazione in tempo reale delle top 3 notizie crypto tramite GNews.

## 🛠️ Tech Stack & Architettura

Il progetto è costruito per essere **serverless, gratuito e completamente automatizzato**:

- **Linguaggio**: Python 3.10
- **Automazione**: GitHub Actions (Cron Job giornaliero)
- **Data Fetching**: `requests` (REST API), `yfinance` (Dati macro)
- **API Integrate**: CoinGecko (Crypto), Alternative.me (Sentiment), GNews (News), Yahoo Finance (Macro)
- **Sicurezza**: Gestione delle chiavi API tramite GitHub Secrets (Nessuna credenziale hardcoded)

##  Come Funziona

1. **Trigger**: GitHub Actions attiva lo script Python ogni giorno alle 07:30 (CET).
2. **Raccolta Dati**: Il bot interroga le API esterne in sequenza, gestendo i rate-limit e utilizzando eccezioni (`try-except`) per garantire l'invio del messaggio anche in caso di fallback di un singolo servizio.
3. **Formattazione**: I dati grezzi vengono elaborati, convertiti in Euro e formattati in Markdown.
4. **Consegna**: Il report finale viene inviato tramite Telegram Bot API.

## 🔧 Setup per Sviluppatori

1. Clona il repository.
2. Crea un bot su Telegram tramite `@BotFather` e ottieni il `TELEGRAM_TOKEN`.
3. Ottieni una API Key gratuita da [GNews.io](https://gnews.io/).
4. Aggiungi le chiavi ai **GitHub Secrets** (`TELEGRAM_TOKEN` e `GNEWS_API_KEY`).
5. Esegui il workflow manualmente o attendi il trigger schedulato.

---
*Progettato e sviluppato da [Il Tuo Nome] - [Link al tuo profilo LinkedIn]*
