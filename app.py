import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Lee las variables de entorno de Render
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "mi_token_secreto_123")
ACCESS_TOKEN = os.getenv("EAAL4JzZBA4ScBSucwDGfrY3e3rbA0xn7QUN7jlB16zUS5Byb5xqNRXojAUEhpbneY8zimAzu5na3ArZBTJPg1QrYpgOSBxZAGBy1c2pZAe5wO7PUXoZACKPRlJZBCwYuOTyizAmILdnoSDcnJwBv5E07S1GN6VbUIA6ZCZBlVaUOpa2ixjqwrsKxFIAIPFXELWEp3o00aEUyEoNrc1SOPAx9s55ZAjtkuboeqgmyvZCOK4n9rXwV7wL4sZC9aUBZBUMKcaj2BjZA0r52YYZBU0OuA8pZAUY")
PHONE_NUMBER_ID = os.getenv("1339587709235147")

@app.route("/", methods=["GET"])
def home():
    return "El servidor de Flask está activo y funcionando correctamente.", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # 1. Verificación del Webhook (GET que hace Meta al guardar la URL)
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode and token:
            if mode == "subscribe" and token == VERIFY_TOKEN:
                print("WEBHOOK_VERIFIED")
                return challenge, 200
            else:
                return "Error de verificación", 403
        return "Parámetros incompletos", 400

    # 2. Recepción de mensajes (POST que manda Meta cuando te escriben)
    elif request.method == "POST":
        data = request.json
        print("Datos recibidos de Meta:", data)

        try:
            # Validar si el JSON contiene un mensaje de WhatsApp válido
            if (
                data.get("entry")
                and data["entry"][0].get("changes")
                and data["entry"][0]["changes"][0].get("value")
                and data["entry"][0]["changes"][0]["value"].get("messages")
            ):
                phone_number_id = data["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
                from_number = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
                msg_body = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                
                print(f"Mensaje recibido de {from_number}: {msg_body}")

                # Aquí puedes agregar la lógica para responder con la API de Meta
                # ...

        except Exception as e:
            print(f"Error procesando el mensaje: {e}")

        return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
