import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Reemplaza con tus datos reales del panel de Meta
TOKEN = "EAAL4JzZBA4ScBSucwDGfrY3e3rbA0xn7QUN7jlB16zUS5Byb5xqNRXojAUEhpbneY8zimAzu5na3ArZBTJPg1QrYpgOSBxZAGBy1c2pZAe5wO7PUXoZACKPRlJZBCwYuOTyizAmILdnoSDcnJwBv5E07S1GN6VbUIA6ZCZBlVaUOpa2ixjqwrsKxFIAIPFXELWEp3o00aEUyEoNrc1SOPAx9s55ZAjtkuboeqgmyvZCOK4n9rXwV7wL4sZC9aUBZBUMKcaj2BjZA0r52YYZBU0OuA8pZAUY"
PHONE_NUMBER_ID = "1339587709235147"
VERIFY_TOKEN = "mi_token_secreto_123" # Puedes dejar este o cambiarlo

@app.route("/webhook", methods=["GET"])
def verificar_webhook():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge
    return "Error de verificación", 403

@app.route("/webhook", methods=["POST"])
@app.route("/webhook", methods=["POST"])
def recibir_mensaje():
    data = request.json
    print("DATOS RECIBIDOS DE META:", data) # Esto saldrá en los Logs de Render
    
    try:
        # Verificamos si realmente viene un mensaje de texto o interactivo
        entry = data.get('entry', [])
        for ent in entry:
            changes = ent.get('changes', [])
            for change in changes:
                value = change.get('value', {})
                
                # Si no hay mensajes (ej: estados de visto), ignoramos para que no falle
                if 'messages' not in value:
                    return jsonify({"status": "ignored"}), 200
                
                mensaje = value['messages'][0]
                numero_remitente = mensaje['from']
                tipo_mensaje = mensaje['type']
                
                # Si el usuario escribe texto plano
                if tipo_mensaje == "text":
                    texto_usuario = mensaje['text']['body'].lower()
                    if "hola" in texto_usuario:
                        enviar_menu_opciones(numero_remitente)
                    else:
                        enviar_mensaje_texto(numero_remitente, "Escribe 'hola' para ver el menú principal.")
                        
                # Si el usuario presiona un botón del menú
                elif tipo_mensaje == "interactive":
                    opcion_seleccionada = mensaje['interactive']['button_reply']['id']
                    
                    if opcion_seleccionada == "opcion_1":
                        enviar_mensaje_texto(numero_remitente, "Has elegido la opción 1: Ventas. ¿En qué podemos colaborarte?")
                    elif opcion_seleccionada == "opcion_2":
                        enviar_mensaje_texto(numero_remitente, "Has elegido la opción 2: Soporte Técnico.")
                    elif opcion_seleccionada == "opcion_3":
                        enviar_mensaje_texto(numero_remitente, "Has elegido la opción 3: Hablar con un asesor.")
                        
    except Exception as e:
        print("Error procesando el mensaje:", e)

    return jsonify({"status": "success"}), 200

def enviar_menu_opciones(destinatario):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": destinatario,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "¡Hola! Bienvenido. Por favor, selecciona una opción:"
            },
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "opcion_1", "title": "1. Ventas"}},
                    {"type": "reply", "reply": {"id": "opcion_2", "title": "2. Soporte"}},
                    {"type": "reply", "reply": {"id": "opcion_3", "title": "3. Asesor"}}
                ]
            }
        }
    }
    requests.post(url, headers=headers, json=payload)

def enviar_mensaje_texto(destinatario, texto):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": destinatario,
        "text": {"body": texto},
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
