# forwarder_a_to_b.py
import json, time, stomp

# ===== Config fija =====
A_HOST, A_PORT, A_USER, A_PASS, A_DEST_IN = "127.0.0.1", 61613, "admin", "admin", "/queue/sensor.in"
B_HOST, B_PORT, B_USER, B_PASS, B_DEST_OUT = "127.0.0.1", 61614, "admin", "admin", "/queue/sensor.out"
ID_SENSOR = "003"  # fallback si faltara

class Forwarder(stomp.ConnectionListener):
    def __init__(self, connA, connB):
        self.connA = connA
        self.connB = connB

    def on_message(self, frame):
        try:
            raw = frame.body
            print(f"[Broker A] Recibido: {raw}")

            try:
                data = json.loads(raw)
            except Exception:
                data = {"mensaje": raw}

            # Eliminar timestamp si viene
            if "timestamp" in data:
                del data["timestamp"]

            # Asegurar id_sensor
            if not data.get("id_sensor"):
                data["id_sensor"] = ID_SENSOR

            out = json.dumps(data, ensure_ascii=False)
            self.connB.send(
                destination=B_DEST_OUT,
                body=out,
                headers={"content-type": "application/json;charset=UTF-8"}
            )
            print(f"[Broker B] Enviado: {out}")

        except Exception as e:
            print("[Forwarder] Error procesando:", e)

def conectar(host, port, user, password):
    c = stomp.Connection([(host, port)])
    c.connect(user, password, wait=True)
    return c

if __name__ == "__main__":
    connB = conectar(B_HOST, B_PORT, B_USER, B_PASS)
    connA = stomp.Connection([(A_HOST, A_PORT)])
    connA.set_listener("", Forwarder(connA, connB))
    connA.connect(A_USER, A_PASS, wait=True)
    connA.subscribe(destination=A_DEST_IN, id="fw1", ack="auto")

    print(f"[Forwarder] A {A_HOST}:{A_PORT} {A_DEST_IN} → B {B_HOST}:{B_PORT} {B_DEST_OUT}. Ctrl+C para salir.")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        connA.disconnect(); connB.disconnect()
        print("\n[Forwarder] Finalizado.")
