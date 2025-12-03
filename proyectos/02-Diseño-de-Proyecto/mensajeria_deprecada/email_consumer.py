import stomp, time, smtplib, os
from email.mime.text import MIMEText

# === Config ActiveMQ ===
BROKER_HOST = os.getenv("AMQ_HOST", "127.0.0.1")
BROKER_PORT = int(os.getenv("AMQ_PORT", "61613"))
USER = os.getenv("AMQ_USER", "admin")
PASS = os.getenv("AMQ_PASS", "admin")
DEST = os.getenv("AMQ_DEST", "/queue/alerts.eventosGlobales")

# === Config SMTP (Configuración por defecto para MailHog) ===
# MailHog usa 127.0.0.1:1025 y NO requiere usuario/contraseña ni TLS.
# Para usar Gmail, debes establecer las variables de entorno: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_TLS.
SMTP_HOST = os.getenv("SMTP_HOST", "127.0.0.1")  # <-- Cambiado a localhost para MailHog
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025")) # <-- Cambiado a puerto 1025 para MailHog
SMTP_USER = os.getenv("SMTP_USER", "")          # <-- Vaciado, ya que MailHog no requiere
SMTP_PASS = os.getenv("SMTP_PASS", "")          # <-- Vaciado, ya que MailHog no requiere
TO_EMAIL = os.getenv("TO_EMAIL", "test@mailhog.local")
FROM_EMAIL = os.getenv("FROM_EMAIL", "alertas@sistema.local")
USE_TLS = os.getenv("SMTP_TLS", "false").lower() == "true" # <-- Cambiado a 'false' por defecto para MailHog

class Listener(stomp.ConnectionListener):
    def on_error(self, frame):
        print('Error:', frame.body)
    def on_message(self, frame):
        body = frame.body
        print('Mensaje recibido ->', body)
        send_email(body)

def send_email(texto):
    msg = MIMEText(texto, 'plain', 'utf-8')
    msg['Subject'] = 'Alerta: Don Juan llegó a la salida'
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    # Conecta al servidor SMTP configurado (por defecto 127.0.0.1:1025 para MailHog)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        
        if USE_TLS:
            s.starttls()
            print('Usando TLS.')
        
        # Se intenta el login SOLO si el usuario y contraseña están definidos
        # (Esto es útil si quieres cambiar fácilmente a un servidor real como Gmail)
        if SMTP_USER and SMTP_PASS:
             # Nota: La autenticación FALLARÁ si intentas hacer login en MailHog.
             # Si estás en MailHog, asegúrate que SMTP_USER y SMTP_PASS estén vacíos.
            print('Intentando autenticación...')
            s.login(SMTP_USER, SMTP_PASS)
        else:
            print('Saltando autenticación (ideal para MailHog).')
            
        s.send_message(msg)
        print('Correo enviado a', TO_EMAIL)

if __name__ == '__main__':
    conn = stomp.Connection([(BROKER_HOST, BROKER_PORT)])
    conn.set_listener('', Listener())
    conn.connect(USER, PASS, wait=True)
    conn.subscribe(destination=DEST, id='1', ack='auto')
    print(f'Escuchando {DEST} en {BROKER_HOST}:{BROKER_PORT}. Ctrl+C para salir.')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        conn.disconnect()
