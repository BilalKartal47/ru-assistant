from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Telegram Ayarları
BOT_TOKEN = '7594894142:AAF4nF4wi3HcwBnWxvHMJOPwawgswDUpG4c'
BERA_USER_ID = '1163110782'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

# Telegram Komut Yorumlayıcı
def ru_alpha_response(command):
    if command == '/rû15':
        return "📊 Rû 15 + Alpha analiz çalıştırılıyor...\nBTC: %82 long ihtimali | Giriş: 107.100 | Stop: 106.480 | TP1: 108.800"
    elif command == '/btc':
        return "₿ BTC Anlık Durum:\nFiyat: 107.100\nTrend: Pozitif\nSinyal: Öncü long aktif 🟢"
    elif command == '/pozisyonlarım':
        return "📌 Aktif Pozisyonlar:\n- BTC Long\n  Giriş: 107.100\n  Stop: 106.480\n  Hedef: 108.800"
    elif command == '/test':
        return "📢 Anlık test bildirimi: Rû Assistant aktif durumda ve mesaj gönderiyor 🔔"
    elif command == '/aktif':
        return "▶️ İzleme yeniden başlatıldı. Tüm sinyaller takip ediliyor."
    elif command == '/dur':
        return "⏸️ İzleme durduruldu. Sinyal takibi pasif."
    elif command == '/oneri':
        return "💡 Önerilen Coinler:\n- BTC (Long)\n- ETH (Teyit bekliyor)\n- RUNE (Hacim artışı var)"
    elif command == '/yardim':
        return "🤖 Rû Assistant Komutları:\n/rû15\n/btc\n/pozisyonlarım\n/test\n/dur\n/aktif\n/oneri"
    else:
        return "❓ Komut anlaşılamadı. Yardım için /yardim yaz."

# Telegram Webhook
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

# Gizli Anahtarlı Tetikleyici Endpoint
@app.route('/ru_trigger', methods=['POST'])
def ru_trigger():
    data = request.json or {}
    secret = data.get('secret', '')
    msg = data.get('message', '📡 Rû Assistant’tan tetikleme bildirimi geldi.')

    if secret != 'BERA_2025_SUPERKEY':
        return '⛔ Yetkisiz erişim: Gizli anahtar hatalı.', 403

    requests.post(f'{TELEGRAM_API_URL}/sendMessage', json={
        'chat_id': BERA_USER_ID,
        'text': msg
    })
    return '✅ Tetikleme başarılı.', 200

# Sunucu çalıştırıcı
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
