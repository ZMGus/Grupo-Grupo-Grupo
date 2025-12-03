# consumer_b_forward.py
import time, stomp

# ==============================
# CONFIG (Broker B)
# ==============================
B_HOST = "127.0.0.1"           # Dirección Broker B
B_PORT = 61614                 # Puerto STOMP Broker B (mapeado en docker-compose)
B_USER = "admin"
B_PASS = "admin"

# Cola donde llega el forwarder A→B
SOURCE_DEST = "/queue/sensor.out"
# Cola a la que reenviamos para el notificador de correo
EMAIL_DEST  = "/queue/alerts.email"

class ForwardAndPrint(stomp.ConnectionListener):
    def __init__(self, conn_send):
        self.conn_send = conn_send

    def on_error(self, frame):
        print("[consumer_b] Error:", frame.body)

    def on_message(self, frame):
        body = frame.body
        # 1) Mostrar por consola
        print(f"[consumer_b] Recibido FINAL en {SOURCE_DEST}: {body}")
        # 2) Reenviar a la cola de email
        self.conn_send.send(
            destination=EMAIL_DEST,
            body=body,
            headers={"content-type": "application/json;charset=UTF-8"}
        )
        print(f"[consumer_b]  Reenviado a {EMAIL_DEST}")

def conectar_broker(host, port, user, password):
    c = stomp.Connection([(host, port)])
    c.connect(user, password, wait=True)
    return c

if __name__ == "__main__":
    print(" Iniciando consumer_b_forward...")
    print(f"Broker B: {B_HOST}:{B_PORT}")
    print(f"Escucho {SOURCE_DEST} y reenvío a {EMAIL_DEST}\n")

    # conexión para enviar (publish) a EMAIL_DEST
    conn_sender = conectar_broker(B_HOST, B_PORT, B_USER, B_PASS)

    # conexión para recibir de SOURCE_DEST
    conn_receiver = stomp.Connection([(B_HOST, B_PORT)])
    conn_receiver.set_listener("", ForwardAndPrint(conn_sender))
    conn_receiver.connect(B_USER, B_PASS, wait=True)
    conn_receiver.subscribe(destination=SOURCE_DEST, id="printer1", ack="auto")

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        conn_receiver.disconnect()
        conn_sender.disconnect()
        print("\n consumer_b_forward detenido correctamente.")
