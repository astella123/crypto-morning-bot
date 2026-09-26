# 🤖 Crypto Morning Bot

Un assistente personale automatizzato che consegna ogni mattina un **Crypto Morning Briefing** professionale direttamente su Telegram. 

Progettato per eliminare il rumore di fondo: invece di aprire 10 app e 20 siti web, il bot sintetizza i dati grezzi in un report chiaro, azionabile e sostenibile, pronto prima dell'apertura dei mercati.

### 📱 Anteprima del Report

![Anteprima Report 1](screenshot.png1.jpg)
![Anteprima Report 2](screenshot.png2.jpg)

---

## ✨ Funzionalità Principali

Il bot genera un report giornaliero strutturato in 5 sezioni chiave:

- 💼 **Portfolio Demo**: Calcolo del valore attuale e delle variazioni (24h e 7d) di un portafoglio fittizio, con prezzo per unità.
- 🔥 **Trending & Top Gainers**: Analisi dell'hype di mercato (ricerche CoinGecko) e delle crypto con le migliori performance settimanali.
- 🌍 **Macro & Contesto**: Monitoraggio di S&P 500 e DXY (Indice del Dollaro) con interpretazione automatica dell'impatto sulle crypto (Semaforo 🟢/🔴).
- 🧠 **Market Sentiment**: Indice Fear & Greed con logica Trend Follower.
- 📰 **Ultime Notizie**: Aggregazione in tempo reale delle top 3 notizie crypto tramite GNews.

## 🛠️ Tech Stack & Architettura

Il progetto è costruito per essere **serverless, gratuito e completamente automatizzato**:

- **Linguaggio**: Python 3.10
- **Automazione**: GitHub Actions (Cron Job giornaliero alle 07:30 CET)
- **Data Fetching**: `requests` (REST API), `yfinance` (Dati macro)
- **API Integrate**: CoinGecko, Alternative.me (Sentiment), GNews (News), Yahoo Finance (Macro)
- **Sicurezza**: Gestione delle chiavi API tramite GitHub Secrets (Zero credenziali hardcoded)
- **Robustezza**: Architettura con gestione delle eccezioni (`try-except`) per garantire l'invio del report anche in caso di down temporaneo di una singola API.

## 🧠 La Logica di Business

Il bot non si limita a mostrare numeri. Interpreta i dati macroeconomici per fornire un contesto immediato:
- **S&P 500 in salita** 🟢 = Sentimento azionario positivo, favorevole alle crypto.
- **DXY (Dollaro) in salita** 🔴 = Dollaro forte, storicamente negativo per le crypto.
- **Fear & Greed > 50** 🟢 = Avidità (Trend positivo).

## 🔧 Setup Rapido

1. Clona il repository.
2. Crea un bot su Telegram (`@BotFather`) e ottieni il `TELEGRAM_TOKEN`.
3. Ottieni una API Key gratuita da [GNews.io](https://gnews.io/).
4. Aggiungi le chiavi ai **GitHub Secrets** (`TELEGRAM_TOKEN` e `GNEWS_API_KEY`).
5. Personalizza il `config.json` con le tue crypto e quantità preferite.

---
*Progettato e sviluppato da Andrea Stella | [Profilo LinkedIn](https://www.linkedin.com/in/andrea-stella-211479413/)*
