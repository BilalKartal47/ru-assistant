from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = '7594894142:AAF4nF4wi3HcwBnWxvHMJOPwawgswDUpG4c'
BERA_USER_ID = '1163110782'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

def ru_alpha_response(command):
    if command == '/rû15':
        return "📊 Rû 15 + Alpha analiz çalıştırılıyor...\nBTC: %82 long ihtimali | Giriş: 107.100 | Stop: 106.480 | TP1: 108.800"
    elif command == '/btc':
        return "₿ BTC Anlık Durum:\nFiyat: 107.100\nTrend: Pozitif\nSinyal: Öncü long aktif 🟢"
    elif command == '/pozisyonlarım':
        return "📌 Aktif Pozisyonlar:\n- BTC Long\n  Giriş: 107.100\n  Stop: 106.480\n  Hedef: 108.800"
    elif command == '/dur':
        return "⏸️ İzleme durduruldu. Sinyal takibi pasif."
    elif command == '/aktif':
        return "▶️ İzleme yeniden başlatıldı. Tüm sinyaller takip ediliyor."
    elif command == '/oneri':
        return "💡 Önerilen Coinler:\n- BTC (Long)\n- ETH (Teyit bekliyor)\n- RUNE (Hacim artışı var)"
    elif command == '/yardim':
        return "🤖 Rû Assistant Komutları:\n/rû15\n/btc\n/pozisyonlarım\n/dur\n/aktif\n/oneri"
    else:
        return "❓ Komut anlaşılamadı. Yardım için /yardim yaz."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message = data.get('message', {})
    chat_id = str(message.get('chat', {}).get('id'))
    text = message.get('text', '')

    if chat_id == BERA_USER_ID:
        reply = ru_alpha_response(text)
    else:
        reply = "⛔ Erişim reddedildi. Bu bot yalnızca Berâ içindir."

    requests.post(f'{TELEGRAM_API_URL}/sendMessage', json={
        'chat_id': chat_id,
        'text': reply
    })
    return 'ok', 200

if __name__ == '__main__':
    app.run()
    import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render PORT değişkenini alır
    app.run(host='0.0.0.0', port=port)

