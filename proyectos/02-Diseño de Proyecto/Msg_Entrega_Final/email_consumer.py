# email_notifier.py
import stomp, time, smtplib, json
from email.mime.text import MIMEText

# ==============================
# CONFIG Broker B (suscripción)
# ==============================
BROKER_HOST = "127.0.0.1"
BROKER_PORT = 61614
USER = "admin"
PASS = "admin"
DEST = "/queue/alerts.email"   # Cola donde llegan las alertas reenviadas

# ==============================
# CONFIG SMTP (MailHog por defecto)
# ==============================
SMTP_HOST = "127.0.0.1"
SMTP_PORT = 1025
SMTP_USER = ""
SMTP_PASS = ""
FROM_EMAIL = "alertas@sistema.local"
TO_EMAIL   = "test@mailhog.local"
USE_TLS    = False

# Diccionario de equivalencias ID → Nombre real
PERSONAS = {
    "001": "Don Juan",
    # Aquí puedes agregar más:
    # "002": "María López",
    # "003": "Pedro Gómez"
}

class Listener(stomp.ConnectionListener):
    def on_error(self, frame):
        print('[email_notifier] Error:', frame.body)

    def on_message(self, frame):
        body = frame.body
        print('[email_notifier] Recibido ->', body)
        procesar_y_enviar(body)

def procesar_y_enviar(raw_body):
    """Procesa el JSON recibido, reemplaza id_persona si corresponde y envía el correo."""
    try:
        data = json.loads(raw_body)
    except json.JSONDecodeError:
        print('[email_notifier] Mensaje no es JSON válido, se enviará tal cual.')
        texto = raw_body
    else:
        # --- reemplazo de id_persona por nombre ---
        if "id_persona" in data:
            id_p = data["id_persona"]
            if id_p in PERSONAS:
                nombre = PERSONAS[id_p]
                # Eliminamos id_persona y agregamos Persona
                del data["id_persona"]
                data["Persona"] = nombre
                print(f"[email_notifier] 🔄 Reemplazado id_persona '{id_p}' → Persona: {nombre}")

        # Prepara el texto legible
        texto = json.dumps(data, ensure_ascii=False, indent=2)

    send_email(texto)

def send_email(texto):
    msg = MIMEText(texto, 'plain', 'utf-8')
    msg['Subject'] = 'Alerta de sensor'
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            if USE_TLS:
                s.starttls()
                print('[email_notifier] TLS activo')
            if SMTP_USER and SMTP_PASS:
                s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
        print('[email_notifier]  Correo enviado a', TO_EMAIL)
        print("Contenido del correo:\n", texto)
    except Exception as e:
        print('[email_notifier] Error enviando correo:', e)

if __name__ == '__main__':
    print(" Iniciando email_notifier...")
    print(f"Broker B: {BROKER_HOST}:{BROKER_PORT}")
    print(f"Suscripto a: {DEST}")
    print(f"SMTP: {SMTP_HOST}:{SMTP_PORT} (MailHog)\n")

    conn = stomp.Connection([(BROKER_HOST, BROKER_PORT)])
    conn.set_listener('', Listener())
    conn.connect(USER, PASS, wait=True)
    conn.subscribe(destination=DEST, id='email1', ack='auto')

    try:
        while True: 
            time.sleep(1)
    except KeyboardInterrupt:
        conn.disconnect()
        print("\n email_notifier detenido correctamente.")
