using UnityEngine;
using System;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

public class distancia_broker : MonoBehaviour
{
    [Header("Referencias en escena")]
    public Transform jugador;     // persona
    public Transform objetivo;    // sensor

    [Header("Intervalo de envío")]
    public float intervalo = 10f;
    private float temporizador;

    [Header("Identificadores")]
    public string id_persona = "001";
    public string id_sensor  = "003";

    [Header("Broker A (STOMP)")]
    public string brokerHost = "127.0.0.1";
    public int brokerPort = 61613;
    public string brokerUser = "admin";
    public string brokerPass = "admin";
    public string destination = "/queue/sensor.in";

    void Start() => temporizador = intervalo;

    void Update()
    {
        temporizador -= Time.deltaTime;
        if (temporizador <= 0f)
        {
            temporizador = intervalo;
            EnviarMensaje();
        }
    }

    void EnviarMensaje()
    {
        if (jugador == null || objetivo == null)
        {
            Debug.LogWarning("[Sensor] Falta asignar jugador u objetivo.");
            return;
        }

        float distancia = Vector3.Distance(jugador.position, objetivo.position);

        // JSON sin timestamp
        string json = $"{{\"id_persona\":\"{id_persona}\",\"id_sensor\":\"{id_sensor}\",\"distancia\":{distancia.ToString("F3", System.Globalization.CultureInfo.InvariantCulture)}}}";

        Debug.Log($"[Sensor] Enviando al broker: {json}");
        _ = EnviarStompAsync(json);
    }

    private async Task EnviarStompAsync(string body)
    {
        try
        {
            using var client = new TcpClient();
            await client.ConnectAsync(brokerHost, brokerPort);
            using var stream = client.GetStream();

            string connectFrame =
                "CONNECT\n" +
                "accept-version:1.2\n" +
                $"host:{brokerHost}\n" +
                $"login:{brokerUser}\n" +
                $"passcode:{brokerPass}\n\n" +
                "\0";
            byte[] connectBytes = Encoding.ASCII.GetBytes(connectFrame);
            await stream.WriteAsync(connectBytes, 0, connectBytes.Length);

            byte[] buf = new byte[256];
            int n = await stream.ReadAsync(buf, 0, buf.Length);
            string resp = Encoding.ASCII.GetString(buf, 0, n);
            if (!resp.Contains("CONNECTED"))
            {
                Debug.LogError("[Sensor] No se recibió CONNECTED del broker.");
                return;
            }

            byte[] bodyBytes = Encoding.UTF8.GetBytes(body);
            string header =
                "SEND\n" +
                $"destination:{destination}\n" +
                "content-type:application/json;charset=UTF-8\n" +
                $"content-length:{bodyBytes.Length}\n\n";
            byte[] headerBytes = Encoding.ASCII.GetBytes(header);

            await stream.WriteAsync(headerBytes, 0, headerBytes.Length);
            await stream.WriteAsync(bodyBytes, 0, bodyBytes.Length);
            await stream.WriteAsync(new byte[] { 0 }, 0, 1);
            await stream.FlushAsync();

            Debug.Log("[Sensor] Mensaje enviado correctamente.");
        }
        catch (Exception ex)
        {
            Debug.LogError("[Sensor] Error enviando a ActiveMQ: " + ex.Message);
        }
    }
}
