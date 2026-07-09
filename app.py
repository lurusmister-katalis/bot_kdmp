from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- PASTIKAN MENGISI TOKEN DAN LINK FORM DI BAWAH INI ---
FONNTE_TOKEN = "8eeBxZjLWATCUBHn2R7k"
LINK_GOOGLE_FORM = "https://forms.gle/h9Lu73KtUKCbigtB8"

# Dictionary untuk menyimpan status percakapan tiap user
# Format: {'nomor_wa': 'status'}
user_state = {}

def send_whatsapp_message(target, message):
    url = "https://api.fonnte.com/send"
    headers = {
        "Authorization": FONNTE_TOKEN
    }
    data = {
        "target": target,
        "message": message
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        return response.json()
    except Exception as e:
        print(f"Error mengirim pesan ke Fonnte: {e}")
        return None

@app.route('/webhook', methods=['POST'])
def webhook():
    # Mengambil data dari Fonnte
    if request.is_json:
        data = request.json
    else:
        data = request.form

    sender = data.get('sender')
    message = data.get('message', '').lower()

    print("\n=== PESAN MASUK DARI FONNTE ===")
    print(f"Pengirim : {sender}")
    print(f"Isi Pesan: {message}")
    print("===============================\n")

    if not sender or not message:
        print("INFO: Data pengirim atau pesan tidak terbaca.")
        return jsonify({"status": "failed", "reason": "No sender or message"}), 400

    # Mengecek status user saat ini dari memori (Dictionary)
    status_saat_ini = user_state.get(sender)

    # SKENARIO 2: Jika user sebelumnya sudah disapa dan sedang menunggu isi form
    # Apapun balasannya (ok, sudah, beres, p, stiker, dll), bot akan balas terima kasih
    if status_saat_ini == 'menunggu_form':
        reply = (
            "Terima kasih sudah mengisi form pesanan Anda! \n"
            "Pesanan Anda akan segera kami rekap dan proses. Kami akan menghubungi Anda kembali untuk total tagihan."
        )
        print("Skenario 2 dieksekusi. User mengonfirmasi form.")
        send_whatsapp_message(sender, reply)
        
        # Hapus memori user ini agar siklus kembali dari awal jika dia chat lagi besok/nanti
        user_state.pop(sender, None)

    # SKENARIO 1: Jika user belum ada di memori (chat pertama kali)
    # Apapun sapaannya (assalamualaikum, p, halo, dll), bot akan kasih link
    else:
        reply = (
            "Halo selamat datang di toko sembako.\n"
            f"Silahkan isi Google Form ini untuk order: {LINK_GOOGLE_FORM}\n\n"
            "Jika sudah isi, silakan balas chat ini dengan kata apa saja (misal: 'ok' atau 'sudah')."
        )
        print("Skenario 1 dieksekusi. Menyapa user baru.")
        send_whatsapp_message(sender, reply)
        
        # Simpan nomor user ke memori dengan status 'menunggu_form'
        user_state[sender] = 'menunggu_form'

    return jsonify({"status": "success"}), 200
