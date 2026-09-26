import requests

# Il token che abbiamo verificato funzionare nel browser
token = "8912873384:AAHPUXlXVxaMN1XBqO8cyz3ssdQL59sDGAo"
chat_id = "8582302114"

url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=FINALMENTE_FUNZIONA"
risposta = requests.get(url)

print(risposta.text)
